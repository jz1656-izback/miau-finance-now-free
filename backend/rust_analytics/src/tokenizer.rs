use pyo3::prelude::*;

pub struct SimpleTokenizer;

impl SimpleTokenizer {
    pub fn tokenize(text: &str) -> Vec<String> {
        let mut tokens = Vec::new();
        let mut current = String::new();
        for ch in text.chars() {
            if ch.is_alphanumeric() || ch == '\'' {
                current.push(ch);
            } else {
                if !current.is_empty() {
                    tokens.push(current.clone());
                    current.clear();
                }
                if !ch.is_whitespace() {
                    tokens.push(ch.to_string());
                }
            }
        }
        if !current.is_empty() {
            tokens.push(current);
        }
        tokens
    }

    pub fn count_tokens(text: &str) -> usize {
        Self::tokenize(text).len()
    }
}

#[pyfunction]
fn tokenize(text: &str) -> Vec<String> {
    SimpleTokenizer::tokenize(text)
}

#[pyfunction]
fn count_tokens(text: &str) -> usize {
    SimpleTokenizer::count_tokens(text)
}

pub fn register( m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tokenize, m)?)?;
    m.add_function(wrap_pyfunction!(count_tokens, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize_simple() {
        let tokens = SimpleTokenizer::tokenize("hello world");
        assert_eq!(tokens, vec!["hello", "world"]);
    }

    #[test]
    fn test_tokenize_punctuation() {
        let tokens = SimpleTokenizer::tokenize("hello, world!");
        assert_eq!(tokens, vec!["hello", ",", "world", "!"]);
    }

    #[test]
    fn test_tokenize_contraction() {
        let tokens = SimpleTokenizer::tokenize("don't stop");
        assert_eq!(tokens, vec!["don't", "stop"]);
    }

    #[test]
    fn test_tokenize_empty() {
        let tokens = SimpleTokenizer::tokenize("");
        assert!(tokens.is_empty());
    }

    #[test]
    fn test_tokenize_whitespace() {
        let tokens = SimpleTokenizer::tokenize("  a  b  ");
        assert_eq!(tokens, vec!["a", "b"]);
    }

    #[test]
    fn test_count_tokens() {
        assert_eq!(SimpleTokenizer::count_tokens("hello world"), 2);
        assert_eq!(SimpleTokenizer::count_tokens(""), 0);
        assert_eq!(SimpleTokenizer::count_tokens("a b c d e"), 5);
    }
}
