"""
Stack CDK: S3 + CloudFront para hospedar Flappy Kiro como juego web.

Recursos creados:
  - S3 Bucket (privado, acceso solo via CloudFront OAC)
  - CloudFront Distribution con OAC
  - Bucket Policy que permite solo a CloudFront leer el bucket
"""
import aws_cdk as cdk
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct


class FlappyKiroHostingStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── S3 Bucket ────────────────────────────────────────────────────────
        bucket = s3.Bucket(
            self,
            "FlappyKiroBucket",
            bucket_name=None,          # Nombre auto-generado para evitar conflictos
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,   # Para facilitar cleanup en dev
            auto_delete_objects=True,               # Lambda helper para vaciar el bucket
        )

        # ── CloudFront Origin Access Control (OAC) ───────────────────────────
        # OAC es el método moderno recomendado por AWS (reemplaza OAI)
        oac = cloudfront.CfnOriginAccessControl(
            self,
            "FlappyKiroOAC",
            origin_access_control_config=cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name="FlappyKiroOAC",
                origin_access_control_origin_type="s3",
                signing_behavior="always",
                signing_protocol="sigv4",
                description="OAC para Flappy Kiro S3 bucket",
            ),
        )

        # ── CloudFront Distribution ───────────────────────────────────────────
        distribution = cloudfront.Distribution(
            self,
            "FlappyKiroDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                compress=True,
            ),
            default_root_object="index.html",
            error_responses=[
                # SPA fallback: rutas desconocidas → index.html
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
            ],
            comment="Flappy Kiro - Pygame/WASM web game",
        )

        # Asociar OAC a la distribución (L1 escape hatch)
        cfn_distribution = distribution.node.default_child
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.OriginAccessControlId",
            oac.get_att("Id"),
        )
        # Eliminar el OAI legacy que el L2 agrega por defecto
        cfn_distribution.add_property_override(
            "DistributionConfig.Origins.0.S3OriginConfig.OriginAccessIdentity",
            "",
        )

        # ── Bucket Policy: solo CloudFront puede leer ─────────────────────────
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="AllowCloudFrontServicePrincipal",
                effect=iam.Effect.ALLOW,
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                actions=["s3:GetObject"],
                resources=[bucket.arn_for_objects("*")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": self.format_arn(
                            service="cloudfront",
                            region="",
                            resource=f"distribution/{distribution.distribution_id}",
                        )
                    }
                },
            )
        )

        # ── Outputs ───────────────────────────────────────────────────────────
        CfnOutput(
            self,
            "BucketName",
            value=bucket.bucket_name,
            description="Nombre del S3 bucket donde se sube el build",
            export_name="FlappyKiroBucketName",
        )

        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="URL pública del juego",
            export_name="FlappyKiroURL",
        )

        CfnOutput(
            self,
            "DistributionId",
            value=distribution.distribution_id,
            description="ID de la distribución CloudFront (para invalidar cache)",
            export_name="FlappyKiroDistributionId",
        )
