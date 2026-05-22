# Lynceus Project Instructions

This document provides context and guidelines for the Lynceus project. As the project evolves, this file should be updated to reflect the current state of the architecture, tech stack, and development workflows.

## Project Overview
**Vision:** In Greek myth, the Argonaut Lynceus had eyesight so keen he could see through walls and into the earth itself. Nothing stayed hidden from him. This tool brings the same scrutiny to your browser extensions, seeing past what they claim to be and catching what they're really doing.

Lynceus is a security analysis tool designed to scrutinize browser extensions, VS Code extensions, and NPM packages for malware.

### Key Features
- **Discovery:** Automatically identifies extensions and packages to scan by importing VS Code settings and parsing `package.json` or `package-lock.json` files.
- **Initial Scanning:** Uses a local Anti-Virus (AV) engine for rapid, offline checks.
- **Static Analysis:** Integrates Semgrep for deep security audits, identifying dangerous code patterns, secrets, and vulnerabilities in discovered packages.
- **Escalation:** Suspicious or ambiguous findings are automatically uploaded to VirusTotal for comprehensive multi-engine analysis.
- **Deep Scrutiny:** Focuses on behavioral analysis beyond simple static signatures.
- **Notifications:** Supports sending email alerts summarizing scan results or flagging immediate threats.

### Input Sources
- **VS Code:** Imports extension lists from local settings files.
- **NPM:** Parses `package.json` and `package-lock.json` for dependency lists.
- **Manual:** (Planned) Option to provide a direct path to an extension or package file.

### Target Platforms
- Browser Extensions (Chrome, Firefox, etc.)
- VS Code Extensions
- NPM Packages

## Architecture & Tech Stack
- **Language:** Python 3.x
- **AV Integration:** Local AV (e.g., ClamAV) via subprocess.
- **Static Analysis:** Semgrep (security-audit and secrets rulesets).
- **APIs:** VirusTotal API (via `requests`)
- **Notifications:** SMTP via standard Python libraries (SendGrid/AgentMail compatible).

## Building and Running
*No build or execution scripts have been identified yet.*

- **Build:** `[TODO: Add build command]`
- **Run:** `[TODO: Add run command]`
- **Test:** `[TODO: Add test command]`

## Development Conventions
- **Engineering Standards:**
    - **Linting:** Pylint score must be at least **9/10** (excluding "fixme" warnings for TODOs).
    - **Testing:** All tests must pass for any submission.
    - **Coverage:** Unit tests must cover at least **90%** of all code pathways (aim for 100%).
    - **Documentation:** READMEs and `GEMINI.md` must be updated concurrently with code changes.
- **Security First:** Handle all scanned samples as potentially malicious. Use sandboxing or isolated environments for analysis.
- **API Hygiene:** Never commit VirusTotal API keys to the repository. Use environment variables.

## Documentation
- [TODO: Add links to internal documentation or design docs]
