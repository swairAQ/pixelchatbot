# Deployment Guide for Pixel Chat 💖

This guide covers free hosting options to deploy your Streamlit chatbot so your friends can use it!

## 🎯 Best Option: Streamlit Community Cloud (FREE & Official)

**Streamlit Community Cloud** is the easiest and best option for Streamlit apps. It's 100% free and specifically designed for Streamlit.

### Setup Steps:

1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push your code (make sure `.env` is in `.gitignore` - it already is!)
2. **Sign up for Streamlit Community Cloud**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign up with your GitHub account
   - Authorize Streamlit to access your repositories

3. **Deploy your app**

   - Click "New app"
   - Select your repository
   - Set main file path to: `app.py`
   - Add your secrets (API keys):
     - Go to "Advanced settings" → "Secrets"
     - Add:
       ```
       OPENAI_API_KEY=your_api_key_here
       OPENAI_BASE_URL=your_base_url_here (optional)
       OPENAI_MODEL=gpt-3.5-turbo (optional)
       ```
   - Click "Deploy"

4. **Share the URL**
   - Your app will be live at: `https://your-app-name.streamlit.app`
   - Share this URL with your friends!

**Note**: Make sure your `requirements.txt` is up to date!

---

## 🌐 Alternative Options

### Option 2: Render (FREE Tier Available)

**Steps:**

1. Sign up at [render.com](https://render.com) (free tier available)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL` (optional)
   - `OPENAI_MODEL` (optional)
6. Deploy!

**Note**: Free tier spins down after 15 minutes of inactivity, so there's a ~30 second cold start.

---

### Option 3: Railway (FREE Tier Available)

**Steps:**

1. Sign up at [railway.app](https://railway.app)
2. Create new project → "Deploy from GitHub repo"
3. Add environment variables in the dashboard
4. Railway auto-detects Streamlit and deploys!

**Note**: Railway has a generous free tier with $5/month credit.

---

### Option 4: Fly.io (FREE Tier Available)

**Steps:**

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. Create `fly.toml` (see below)
4. Deploy: `fly deploy`

**Note**: Free tier includes 3 shared VMs.

---

### Option 5: PythonAnywhere (FREE Tier Available)

**Steps:**

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via the web interface
3. Create a web app (Flask) but run Streamlit via Bash console
4. Note: Free tier has limitations (websites sleep after inactivity)

---

## 📝 Important Notes

### Environment Variables

Your app uses environment variables for API keys. Make sure to set these in your hosting platform:

- `OPENAI_API_KEY` (required)
- `OPENAI_BASE_URL` (optional, for custom endpoints)
- `OPENAI_MODEL` (optional, defaults to gpt-3.5-turbo)

### Files to Deploy

✅ DO deploy:

- `app.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

❌ DON'T deploy (already in `.gitignore`):

- `.env` file (use platform secrets instead)
- `conversations.json` (will be created on first use)
- `preferences.json` (will be created on first use)

### Security

- Never commit `.env` files to Git (already in `.gitignore`)
- Use your hosting platform's secrets/environment variables feature
- Keep your API keys private!

---

## 🚀 Quick Deploy Checklist

- [ ] Code is on GitHub
- [ ] `.env` is in `.gitignore` ✅ (already done)
- [ ] `requirements.txt` is updated ✅
- [ ] Environment variables are configured in hosting platform
- [ ] App is deployed and accessible
- [ ] Tested the deployed app
- [ ] Shared URL with friends! 💖

---

## 💡 Recommendation

**Use Streamlit Community Cloud** - it's the easiest, officially supported, and specifically designed for Streamlit apps. Deployment takes about 5 minutes!
