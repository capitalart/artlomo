# DreamArtMachine Setup Handover for Copilot

Date: 2026-03-24
Owner: Robin / ArtLomo
Target domain: dreamartmachine.com
Target IP: 34.129.216.126
Existing production domain on same server: artlomo.com

## 1) Mission

Set up dreamartmachine.com on the same VM currently serving artlomo.com, with production-safe isolation so no existing ArtLomo services are disrupted.

The server currently has DNS pointed to 34.129.216.126 but no folder or domain config is set up for dreamartmachine.com.

## 2) Critical constraints

1. Do not break or restart critical artlomo.com services unless explicitly required and approved.
2. Back up all edited config files before changing them.
3. Keep dreamartmachine.com isolated from ArtLomo runtime paths, virtual env, and Nginx server blocks.
4. Use additive changes only. No destructive cleanup unless approved.
5. Verify each step before moving on.

## 3) Environment context

1. Existing app root: /srv/artlomo
2. Existing stack: Flask + Gunicorn + Nginx on Debian 12 VM
3. IP: 34.129.216.126
4. Goal now: bring dreamartmachine.com online with correct web root and SSL, then prepare deployment-ready app structure.

## 4) Deliverables required

1. Domain resolves and serves HTTP and HTTPS.
2. Dedicated web root created for dreamartmachine.com.
3. Nginx site block added and enabled.
4. SSL certificate issued and auto-renewal verified.
5. Basic landing page online so domain is visibly alive.
6. Optional app scaffold path prepared for future Flask/Node deployment.
7. Written summary of all commands run, files changed, and service status.

## 5) Safe implementation plan

### Phase A: Preflight and backups

1. Confirm DNS from server:
   - dig +short dreamartmachine.com
   - dig +short <www.dreamartmachine.com>
2. Confirm Nginx and existing sites:
   - nginx -t
   - ls -la /etc/nginx/sites-available
   - ls -la /etc/nginx/sites-enabled
3. Backup Nginx config directory:
   - sudo cp -a /etc/nginx /etc/nginx.backup-$(date +%Y%m%d-%H%M%S)

### Phase B: Create domain directories

1. Create folders:
   - /var/www/dreamartmachine.com/public
   - /var/www/dreamartmachine.com/logs
2. Set ownership and permissions:
   - owner www-data:www-data
   - public readable, logs writable for Nginx where needed
3. Add a simple index.html in public with clear DreamArtMachine heading and timestamp.

### Phase C: Add Nginx site (HTTP first)

1. Create /etc/nginx/sites-available/dreamartmachine.com with:
   - server_name dreamartmachine.com <www.dreamartmachine.com>
   - root /var/www/dreamartmachine.com/public
   - index index.html
   - access_log and error_log in /var/www/dreamartmachine.com/logs
2. Enable site by symlink to sites-enabled.
3. Test and reload:
   - sudo nginx -t
   - sudo systemctl reload nginx
4. Validate HTTP with curl and browser.

### Phase D: SSL with Certbot

1. Ensure certbot present:
   - sudo apt-get update
   - sudo apt-get install -y certbot python3-certbot-nginx
2. Issue cert:
   - sudo certbot --nginx -d dreamartmachine.com -d <www.dreamartmachine.com>
3. Verify renewal timer:
   - systemctl status certbot.timer
   - sudo certbot renew --dry-run
4. Re-check:
   - curl -I <https://dreamartmachine.com>

### Phase E: Prepare app deployment path

1. Create app directory for future runtime:
   - /srv/dreamartmachine
2. Create baseline structure:
   - /srv/dreamartmachine/app
   - /srv/dreamartmachine/deploy
   - /srv/dreamartmachine/logs
   - /srv/dreamartmachine/var
3. Add placeholder README with deployment notes.
4. Do not bind Gunicorn/systemd yet unless explicitly requested.

## 6) If planning immediate Flask deployment

Only do this if requested in the same task.

1. Create Python venv under /srv/dreamartmachine/.venv
2. Install Flask + Gunicorn
3. Add minimal app entrypoint and WSGI
4. Add systemd unit dreamartmachine.service on unused socket/port
5. Update Nginx location / to proxy_pass local service
6. Restart service and validate logs

## 7) Validation checklist

1. dreamartmachine.com returns 200 on HTTP and HTTPS.
2. <www.dreamartmachine.com> redirects correctly as intended.
3. SSL cert valid and not self-signed.
4. nginx -t passes.
5. ArtLomo endpoints still reachable and unchanged.
6. No unexpected errors in Nginx logs after reload.

## 8) Rollback plan

1. Disable dreamartmachine.com site symlink.
2. Restore previous Nginx backup from /etc/nginx.backup-TIMESTAMP.
3. nginx -t and reload.
4. Confirm artlomo.com remains healthy.

## 9) Final report format required from Copilot

1. What was created.
2. Full list of changed files with paths.
3. Service status checks.
4. DNS and SSL verification output summary.
5. Remaining optional next steps.

## 10) Copy-paste prompt for next Copilot chat

Use this exact brief in a new chat that has server access:

I need you to set up dreamartmachine.com on my existing VM at 34.129.216.126, where artlomo.com is already running. Do this safely without breaking artlomo.com.

Requirements:

1. Create /var/www/dreamartmachine.com/public and serve a live placeholder page.
2. Add and enable an Nginx server block for dreamartmachine.com and <www.dreamartmachine.com>.
3. Issue SSL with certbot and confirm renew dry run.
4. Validate HTTP and HTTPS responses.
5. Create /srv/dreamartmachine folder structure for future app deployment, but do not migrate or alter artlomo runtime.
6. Back up Nginx config before changes, and provide a rollback path.
7. End with a precise summary of commands run, files changed, and verification results.

Safety constraints:

- Additive changes only.
- No destructive commands.
- Test nginx config before reload.
- Preserve all existing artlomo domain/service behavior.

If DNS for dreamartmachine.com is not resolving to 34.129.216.126, stop and report exactly what is wrong before proceeding.
