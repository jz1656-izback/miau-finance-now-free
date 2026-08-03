# 🐱 MIAU FINANCE — Release Process

## Version Scheme

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, small features
  │     └──────── New features, backwards compatible
  └────────────── Breaking changes, new architecture
```

Current version: **V14 (8 Billion Human Surfaces)**
Previous: V11-V13 (Cat Terminal Supremacy), V10 (Great Absorption), V9 (Global Domination Era)

## Branches

| Branch | Purpose | Deploy |
|--------|---------|--------|
| `main` | Production | Auto-deployed to production |
| `dev` | Development | Active development |
| `preprod` | Pre-release testing | Staging environment |
| `feature/*` | Feature branches | Branch from dev |

## Release Checklist

### For a new version release:

```bash
# 1. Create preprod branch from dev
git checkout dev
git checkout -b release/vX.Y.Z

# 2. Update version in VERSION file
echo "X.Y.Z" > VERSION

# 3. Update CHANGELOG.md
# Add: new features, fixed bugs, breaking changes

# 4. Run full test suite
cd frontend && npm test
cd backend && python -m pytest

# 5. Build and verify
cd frontend && npm run build

# 6. Create pull request to preprod
gh pr create --base preprod --head release/vX.Y.Z

# 7. After preprod approval, merge to main
git checkout main
git merge release/vX.Y.Z
git tag vX.Y.Z
git push origin vX.Y.Z

# 8. Deploy to production
# (depends on infrastructure)

# 9. Update dev branch
git checkout dev
git merge main
```

## Hotfix Process

```bash
git checkout main
git checkout -b hotfix/X.Y.Z+1
# Fix the issue
git commit -m "[hotfix] description"
git checkout main
git merge hotfix/X.Y.Z+1
git checkout dev
git merge hotfix/X.Y.Z+1
```

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| V14 | TBD | MCP Server, SDK, Mobile, Open Source |
| V13 | 2026-05 | AI singularity, multi-model router |
| V12 | 2026-05 | Real-time streaming, new providers |
| V11 | 2026-05 | 17 indicators, econometrics, quant |
| V10 | 2026-05 | Fixed income, ETFs, commodities |
| V9 | 2026-05 | Autonomous wealth, Cat Bank, CFO |
| V8 | 2026-05 | 3D MiauGlobe, 230 courses |
| V7 | 2026-05 | 50+ providers, 30+ endpoints |
| V6 | 2026-05 | Three.js globe, cat army |
| V5 | 2026-03 | 50+ commands, AI, calculators |
| V4 | 2026-02 | Terminal UI, 200+ APIs |
| V3 | 2026-01 | Data source layer |
| V2 | 2025-12 | DeFi, Web3, brokers |
| V1 | 2025-11 | Foundation |

> *"The cat releases often. The cat releases clean. The cat releases with confidence." 🐱*
