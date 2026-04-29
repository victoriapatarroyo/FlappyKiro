# Flappy Kiro — Infraestructura AWS

Stack CDK que crea el hosting para el juego web en AWS.

## Arquitectura

```
GitHub Actions
     │
     ├─ pytest (tests)
     ├─ pygbag --build (compila a WASM)
     ├─ cdk deploy (S3 + CloudFront)
     └─ aws s3 sync (sube el build)

Usuario Browser → CloudFront → S3 Bucket
                  (HTTPS)      (privado)
```

## Recursos AWS creados

| Recurso | Descripción |
|---------|-------------|
| S3 Bucket | Almacena los archivos del juego (privado) |
| CloudFront Distribution | CDN global con HTTPS |
| Origin Access Control | Acceso seguro S3 ↔ CloudFront |

## Setup inicial (una sola vez)

### 1. Prerrequisitos

```bash
# Node.js 20+ y CDK CLI
npm install -g aws-cdk@2

# Python deps del stack
cd infra
pip install -r requirements.txt
```

### 2. Configurar secretos en GitHub

Ve a tu repo → Settings → Secrets and variables → Actions y agrega:

| Secret | Valor |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | Access key de un IAM user con permisos de deploy |
| `AWS_SECRET_ACCESS_KEY` | Secret key correspondiente |
| `AWS_ACCOUNT_ID` | Tu AWS Account ID (12 dígitos) |

### 3. Permisos IAM mínimos para el deploy

El IAM user necesita estos permisos:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "cloudfront:*",
        "iam:*",
        "ssm:GetParameter",
        "ecr:*",
        "lambda:*"
      ],
      "Resource": "*"
    }
  ]
}
```

> Para producción, usa permisos más restrictivos o OIDC con roles temporales.

### 4. Deploy manual (opcional)

```bash
cd infra
cdk bootstrap --context account=<TU_ACCOUNT_ID>
cdk deploy --context account=<TU_ACCOUNT_ID>
```

## CI/CD Flow

```
push a main
    │
    ├── [test]          pytest en ubuntu con SDL dummy
    ├── [build]         pygbag --build → build/web/
    ├── [deploy-infra]  cdk deploy (idempotente)
    └── [deploy-content] s3 sync + CloudFront invalidation
```

Los PRs solo corren `test` y `build` — nunca hacen deploy.

## Teardown

```bash
cd infra
cdk destroy
```

Esto elimina todos los recursos (el bucket tiene `RemovalPolicy.DESTROY`).
