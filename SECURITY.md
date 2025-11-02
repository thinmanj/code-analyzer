# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| < 0.4   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in code-analyzer, please report it by emailing **thinmanj@gmail.com**.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

When reporting a vulnerability, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Release**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next regular release

## Security Best Practices

When using code-analyzer:

1. **Code Anonymization**: Use `--anonymize-for-llm` when sending code to external LLM services
2. **API Keys**: Never commit API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY) to repositories
3. **Privacy**: The tool is read-only and never modifies source code
4. **Local Analysis**: Most analysis runs locally; external LLM features are optional

## Known Security Considerations

- **VCS Analysis**: Reads git history locally; does not transmit to external services
- **Plugin System**: Custom plugins have full access to analyzed code; only use trusted plugins
- **LLM Integration**: Optional feature; code can be anonymized before external analysis
