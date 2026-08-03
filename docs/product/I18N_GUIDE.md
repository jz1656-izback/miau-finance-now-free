# 🐱 MIAU FINANCE — i18n Guide

## 9 Languages · Localized Terminal · Multi-Currency

### Supported Languages
| Code | Language | Status |
|------|----------|--------|
| EN | English | ✅ Complete |
| DE | Deutsch | ✅ Complete |
| FR | Français | ✅ Complete |
| ES | Español | ✅ Complete |
| JA | 日本語 | ✅ Complete |
| ZH | 中文 | ✅ Complete |
| KO | 한국어 | ✅ Complete |
| PT | Português | ✅ Complete |
| RU | Русский | ✅ Complete |

### Change Language
```bash
# In terminal:
lang de     # Switch to German
lang fr     # Switch to French
lang ja     # Switch to Japanese
lang        # Show current language
```

### Currency Support
| Currency | Symbol | Code |
|----------|--------|------|
| Euro | € | EUR |
| US Dollar | $ | USD |
| British Pound | £ | GBP |
| Japanese Yen | ¥ | JPY |
| Swiss Franc | CHF | CHF |
| Chinese Yuan | ¥ | CNY |

### Adding a New Language
1. Edit `frontend/src/lib/i18n.ts`
2. Add translations for all strings
3. Add the locale code to `SUPPORTED_LOCALES`
4. Test in terminal: `lang <code>`

> *"The cat speaks 9 languages. The cat judges your portfolio in all of them." 🐱*
