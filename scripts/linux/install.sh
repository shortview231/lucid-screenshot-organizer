#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
venv="$repo_root/.venv"
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/lucid-screenshot-organizer"
service_dir="$HOME/.config/systemd/user"
service_path="$service_dir/lucid-screenshot-organizer.service"

python3 -m venv "$venv"
"$venv/bin/python" -m pip install --upgrade pip
"$venv/bin/python" -m pip install -e "$repo_root"

mkdir -p "$config_dir" "$service_dir"
if [[ ! -f "$config_dir/config.toml" ]]; then
  cp "$repo_root/config/config.example.toml" "$config_dir/config.toml"
fi

cat > "$service_path" <<EOF
[Unit]
Description=Lucid Screenshot Organizer
After=graphical-session.target

[Service]
Type=simple
ExecStart=$venv/bin/python -m lucid_screenshot_organizer.main
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now lucid-screenshot-organizer.service

echo "Installed Lucid Screenshot Organizer."
echo "Config: $config_dir/config.toml"