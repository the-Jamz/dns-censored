# Contributing to UK-Blocking Hosts DNS Blocklist

Thank you for your interest in contributing! This project tracks websites and services that block or restrict access to UK users.

## 🎯 What Should Be Included

### ✅ Include

- Sites that completely block access from UK IP addresses
- Sites that significantly restrict functionality for UK users
- Services that have withdrawn from the UK market due to Online Safety Act or related regulations
- Sites showing explicit "not available in UK" messages

### ❌ Do Not Include

- Sites that only show cookie/GDPR consent notices
- Sites with UK-specific terms of service (without actual blocking)
- Regional pricing differences
- Content licensing restrictions (e.g., Netflix regional libraries)
- Sites temporarily down or experiencing technical issues

## 📝 How to Contribute

### Reporting a Blocked Site

If you've discovered a site blocking UK users, please [open an issue](https://github.com/the-Jamz/dns-censored/issues/new) with:

1. **Domain name(s)** - All domains affected (e.g., `reddit.com`, `www.reddit.com`, `old.reddit.com`)
2. **Evidence** - Screenshot or description of the blocking message
3. **Date discovered** - When you first noticed the block
4. **Testing method** - How you verified it's UK-specific (e.g., works with VPN, doesn't work without)
5. **Type of block** - Complete block, partial restriction, or functionality limitation

### Submitting a Pull Request

1. **Fork the repository**

2. **Edit the source file** (`domains/uk-blocking-hosts.txt`):
   ```
   # Service Name
   domain.com
   www.domain.com
   subdomain.domain.com
   ```

3. **Update the header**:
   - Increment the entry count
   - Update the last modified date

4. **Commit the source file**:
   ```bash
   git add domains/uk-blocking-hosts.txt
   git commit -m "Add [service name] to blocklist"
   ```

5. **Push and create a pull request**

**Important:** Only commit changes to `domains/uk-blocking-hosts.txt`. The domain list is validated automatically by GitHub Actions. Users generate their own platform-specific configurations using the scripts in the `scripts/` directory.

## 📋 Pull Request Guidelines

### Checklist

- [ ] Domains added to `domains/uk-blocking-hosts.txt`
- [ ] Domains grouped by service with comment header
- [ ] Entry count updated in header
- [ ] Only the source file committed
- [ ] Evidence of blocking provided (issue link or in PR description)

### Commit Message Format

Use clear, descriptive commit messages:

- ✅ `Add Reddit domains to blocklist`
- ✅ `Add Imgur and file-sharing services`
- ❌ `Update list`
- ❌ `Add domains`

## 🔍 Verification Process

All submissions will be reviewed to ensure:

1. The blocking is legitimate and UK-specific
2. The domains are correctly formatted
3. The service hasn't been previously added
4. The blocking is related to UK regulations (not general geo-restrictions)

## 🏗️ Project Structure

```
dns-censored/
├── domains/              # Source domain list (edit this!)
│   └── uk-blocking-hosts.txt
├── scripts/             # Auto-update scripts for routers
│   ├── mikrotik-update.rsc
│   ├── unifi-update.sh
│   └── README.md
├── .github/
│   └── workflows/
│       └── build.yml    # Domain list validation
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## 🤔 Questions?

If you're unsure whether a site should be included or need help with the contribution process, please open an issue and ask!

## 📜 Code of Conduct

- Be respectful and constructive
- Focus on facts and evidence
- Keep discussions on-topic
- No spam or self-promotion

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for helping maintain transparency about UK internet blocking!**
