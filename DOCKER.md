# 🐳 Docker Multi-Stage Build

Este projeto usa **multi-stage build** para criar imagens Docker otimizadas e seguras.

## 🏗️ Arquitetura Multi-Stage

### Estágio 1: Builder
- **Base**: `python:3.11-slim`
- **Propósito**: Instalar dependências Python
- **Inclui**: Build tools (gcc, build-essential)
- **Output**: Pacotes Python compilados

### Estágio 2: Runtime
- **Base**: `python:3.11-slim` (limpa)
- **Propósito**: Imagem final otimizada
- **Inclui**: Apenas runtime necessário
- **Usuário**: `watchdog` (não-root)

## ✅ Benefícios

### 📦 **Tamanho Reduzido**
- Remove build tools da imagem final
- Apenas dependências de runtime
- ~50% menor que single-stage

### 🛡️ **Segurança**
- Usuário não-root (`watchdog`)
- Sem ferramentas de desenvolvimento
- Surface de ataque reduzida

### ⚡ **Performance**
- Layer caching otimizado
- Builds mais rápidos
- Menos transferência de dados

## 🚀 Comandos de Build

```bash
# Build normal (usa multi-stage automaticamente)
docker-compose build

# Build produção
docker-compose -f docker-compose.prod.yml build

# Build manual com tags
docker build -t watchdog:latest .
docker build -t watchdog:prod -f Dockerfile .

# Verificar tamanhos das imagens
docker images watchdog
```

## 📊 Comparação de Tamanhos

| Tipo | Tamanho Estimado | Descrição |
|------|------------------|-----------|
| Single-stage | ~300MB | Com build tools |
| Multi-stage | ~150MB | Sem build tools |
| Redução | ~50% | Economia significativa |

## 🔍 Estrutura de Layers

```dockerfile
# Stage 1: builder (descartado)
FROM python:3.11-slim AS builder
# ... instalar dependências ...

# Stage 2: runtime (final)
FROM python:3.11-slim AS runtime
COPY --from=builder ...
# ... configurar runtime ...
```

## 🔧 Customização

Para modificar o build:

1. **Adicionar dependências**: Edite `requirements.txt`
2. **Modificar runtime**: Ajuste estágio `runtime`
3. **Segurança**: Mantenha usuário `watchdog`
4. **Build tools**: Adicione no estágio `builder`

## 🐳 Best Practices Implementadas

- ✅ Multi-stage build
- ✅ Usuário não-root
- ✅ Layer caching otimizado
- ✅ Minimal runtime dependencies
- ✅ Health checks
- ✅ Proper file permissions
- ✅ Environment variables