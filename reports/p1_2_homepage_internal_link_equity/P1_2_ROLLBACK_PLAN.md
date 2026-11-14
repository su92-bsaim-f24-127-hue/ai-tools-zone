# P1.2 — Emergency Rollback Plan & Runbook

**Project:** AI Tools Zone  
**Production Baseline:** `d3e161862e2008745458915c62a2839bff7988e7`  
**Feature Branch:** `feature/p1-2-homepage-internal-link-equity`  
**Isolated Worktree Path:** `C:\Users\ELITEBOOK\Desktop\AI tools zone-p1-2`  

---

## 1. Operating Context & Safety Status

All P1.2 internal linking modifications exist solely within an isolated Git worktree on branch `feature/p1-2-homepage-internal-link-equity`.

- **NO commits** have been pushed to GitHub.
- **NO merges** have been made into `main`.
- **NO production deployment** has occurred.
- Production at `https://aitoolszone.tech/` remains anchored at `d3e161862e2008745458915c62a2839bff7988e7`.
- The P1.1 branch work in `C:\Users\ELITEBOOK\Desktop\AI tools zone` remains completely untouched.

---

## 2. Emergency Rollback Runbook

To completely discard P1.2 without affecting any other work, execute the following commands in order:

### Step 1: Remove the isolated worktree
```bash
git -C "C:\Users\ELITEBOOK\Desktop\AI tools zone" worktree remove "C:\Users\ELITEBOOK\Desktop\AI tools zone-p1-2" --force
```

### Step 2: Delete the local P1.2 feature branch
```bash
git -C "C:\Users\ELITEBOOK\Desktop\AI tools zone" branch -D feature/p1-2-homepage-internal-link-equity
```

### Step 3: Verify clean baseline status on the repository
```bash
git -C "C:\Users\ELITEBOOK\Desktop\AI tools zone" status
git -C "C:\Users\ELITEBOOK\Desktop\AI tools zone" rev-parse HEAD
# Must confirm baseline: d3e161862e2008745458915c62a2839bff7988e7
```

---

## 3. Verification Post-Rollback
Verify that production baseline `main` remains clean and unaffected:
```bash
git -C "C:\Users\ELITEBOOK\Desktop\AI tools zone" checkout main
python "C:\Users\ELITEBOOK\Desktop\AI tools zone\audit_seo.py"
```
