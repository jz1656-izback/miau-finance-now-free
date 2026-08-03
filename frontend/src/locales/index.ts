import { registerTranslations } from '../lib/i18n'
import en from './en'
import de from './de'
import fr from './fr'
import es from './es'
import ja from './ja'
import zh from './zh'
import ko from './ko'
import pt from './pt'
import ru from './ru'

export function initTranslations(): void {
  registerTranslations('en', en)
  registerTranslations('de', de)
  registerTranslations('fr', fr)
  registerTranslations('es', es)
  registerTranslations('ja', ja)
  registerTranslations('zh', zh)
  registerTranslations('ko', ko)
  registerTranslations('pt', pt)
  registerTranslations('ru', ru)
}
