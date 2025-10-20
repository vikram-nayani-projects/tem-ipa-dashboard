# Deployment Guide - Railway

Quick guide to deploy TEM IPA Manager Dashboard demo to Railway.

## Prerequisites

- GitHub account
- Railway account (free tier is fine)
- Domain access for fishermenfirst.org

---

## Step 1: Push to GitHub (5 minutes)

1. Create new repository on GitHub:
   - Go to github.com
   - Click "New repository"
   - Name: `tem-ipa-dashboard`
   - Visibility: Private (recommended for demo)
   - Don't initialize with README (we already have one)

2. Push local code to GitHub:

```bash
cd C:\Users\vikra\Git\ff-planning

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - TEM IPA demo"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR-USERNAME/tem-ipa-dashboard.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Railway (5 minutes)

1. Go to https://railway.app

2. Sign up/login (use GitHub account for easy connection)

3. Click "New Project"

4. Select "Deploy from GitHub repo"

5. Connect your GitHub account (if not already connected)

6. Select `tem-ipa-dashboard` repository

7. Railway auto-detects Streamlit and starts deployment:
   - Detects `requirements.txt`
   - Installs dependencies
   - Runs `streamlit run src/app.py` automatically

8. Wait 2-3 minutes for build to complete

9. Click the generated URL to test (e.g., `tem-ipa-dashboard.railway.app`)

10. Verify app loads and works correctly

---

## Step 3: Configure Custom Domain (10 minutes)

### In Railway:

1. Go to your project in Railway

2. Click on the service (Streamlit app)

3. Go to "Settings" tab

4. Scroll to "Domains" section

5. Click "Add Custom Domain"

6. Enter: `tem-ipa-demo.fishermenfirst.org`

7. Railway will provide a CNAME target (copy this)
   - Example: `tem-ipa-dashboard.up.railway.app`

### In Your Domain Registrar:

1. Log in to your domain registrar (GoDaddy, Namecheap, etc.)

2. Go to DNS management for `fishermenfirst.org`

3. Add new DNS record:
   - **Type:** CNAME
   - **Host:** tem-ipa-demo
   - **Points to:** [Railway CNAME target from above]
   - **TTL:** 3600 (or default)

4. Save changes

5. Wait 5-30 minutes for DNS propagation

6. Test: Visit `https://tem-ipa-demo.fishermenfirst.org`

7. Verify HTTPS works automatically (Railway provides free SSL)

---

## Step 4: Share with Interview Committee

Once deployed, send the committee:

### Email Template:

```
Subject: TEM IPA Manager Dashboard - Live Demo

Hi [Committee Contact],

I've prepared a live demonstration of the proposed TEM IPA Manager Dashboard
for your review ahead of the interview.

Demo URL: https://tem-ipa-demo.fishermenfirst.org

This proof-of-concept demonstrates:

✅ Real-time vessel trip limit monitoring (4-trip rolling average)
✅ Color-coded compliance status (Green/Yellow/Red)
✅ Next Trip Calculator - Proactive vessel support
✅ Violation detection (Trip Limit + Egregious + MRA)
✅ Data upload interface
✅ Violation reports

Key Features to Review:
1. Fleet Overview - See all vessels at a glance
2. Vessel Details - Select "Northern Star" to see the Next Trip Calculator
3. Violation Reports - Comprehensive violation tracking
4. Upload Data - Mock data import workflow

Note: This uses test data for demonstration. The production system will
integrate with live eLandings data and include authentication, database
persistence, and all features outlined in our proposal.

Please let me know if you have any questions or would like to discuss
specific functionality.

Best regards,
[Your Name]
Fishermen First
```

---

## Troubleshooting

### App won't start on Railway:

**Check build logs:**
1. Go to Railway project
2. Click "Deployments" tab
3. View latest deployment logs
4. Look for errors in dependency installation or startup

**Common fixes:**
- Ensure `requirements.txt` is in root directory
- Verify Python version compatibility (3.8+)
- Check for typos in import statements

### Custom domain not working:

**DNS propagation:**
- Can take 5-60 minutes (sometimes longer)
- Use https://dnschecker.org to verify propagation
- Clear browser cache

**Wrong CNAME:**
- Double-check you copied the exact Railway target
- Ensure no trailing dots or extra spaces
- Format should be: `something.up.railway.app`

### App is slow:

**Railway free tier limits:**
- App "sleeps" after 5 minutes of inactivity
- First load after sleep takes ~30 seconds
- Subsequent loads are fast

**For interview:**
- Visit the URL 2-3 minutes before demo starts
- Keeps app "awake" and responsive

---

## Cost

**Railway Free Tier:**
- ✅ $5/month free credit
- ✅ Enough for demo and initial production use
- ✅ Includes SSL certificate
- ✅ Automatic deployments on git push

**If you exceed free tier:**
- ~$5-10/month for small app
- Can upgrade to paid plan if needed

---

## Updates and Redeployment

**To update the demo:**

1. Make changes locally

2. Push to GitHub:
```bash
git add .
git commit -m "Description of changes"
git push
```

3. Railway automatically redeploys (takes 1-2 minutes)

4. Changes are live at your custom domain

---

## Next Steps After Demo

**If you win the contract:**
- Keep Railway deployment
- Add PostgreSQL database (Railway add-on)
- Implement authentication
- Connect to real eLandings data
- Move from demo subdomain to main domain

**If you don't win:**
- Delete Railway project (no ongoing cost)
- Keep GitHub repo for future use
- Reusable for other fisheries proposals

---

## Ready to Deploy?

1. [ ] Code is in GitHub repo
2. [ ] Railway account created
3. [ ] Project deployed to Railway
4. [ ] Custom domain configured
5. [ ] Demo tested and working
6. [ ] Email sent to committee

**Estimated total time: 20-30 minutes**

Good luck with your demo! 🐟
