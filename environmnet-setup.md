Install WSL 
- wsl --install (via the Windows app "Terminal")
- Restart may be required...
- Set username and password 
Install Docker 
- Install Docker Desktop...in Docker Desktop, do: Settings > Resources > WSL Integration
- Sign into Docker Hub (personal)
- Check Docker and WSL work together
  - From wsl, run: 
    - docker --version
    - docker compose version
    - ping google.com
VSCode set up
- From wsl, run "code ."
- In this (remote) VS code instance(?) install extension ms-vscode-remote.remote-wsl

Set up Git...personal 
- If using Windows side for git (not recommended, because of crlf issues)
  - set up a separate SSH key
  - add separate "alias" github-personal to c:\users\<username>.ssh\config file
  - when clone repo from personal, git clone clone like this: git@github-personal:yourusername/your-repo.git
- If using Linux side
  - set up separate SSH key in /home/<username>/.ssh (make it if it doesn't exist)
  - Run
    - chmod 600 ~/.ssh/id_rsa_personal
	- eval "$(ssh-agent -s)"
    - ssh-add ~/.ssh/id_rsa
	- ssh -T git@github.com (to test)
  - Tip: add the following to the .bashrc file 
    - [ -z "$SSH_AUTH_SOCK" ] && eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa_personal
    
Troubleshooting
- Hung?  From Terminal: "wsl --shutdown"....then relaunch (wsl)