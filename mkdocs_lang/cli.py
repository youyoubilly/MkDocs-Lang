import argparse
from mkdocs_lang.actions import newproject, config, gitclone, cl, newsite
import os

def main(args=None):
    parser = argparse.ArgumentParser(description='Manage multi-language MkDocs projects.')
    subparsers = parser.add_subparsers(dest='action')

    # NewProject action
    newproject_parser = subparsers.add_parser('newproject', help='Create a new project folder with a mkdocs-lang.yml file.')
    newproject_parser.add_argument('--project', required=True, help='Path to the new project')
    newproject_parser.add_argument('--github', help='GitHub account for repository URLs')

    # New action
    newsite_parser = subparsers.add_parser('newsite', help='Create a new MkDocs project.')
    newsite_parser.add_argument('mkdocs_project', help='Name of the MkDocs project')
    newsite_parser.add_argument('--lang', default='en', help='Language code for the MkDocs project')
    newsite_parser.add_argument('--project', help='Path to the main project if not in current directory')

    # Config action
    config_parser = subparsers.add_parser('config', help='Update configuration for the main project.')
    config_parser.add_argument('--project', help='Path to the main project')
    config_parser.add_argument('--github', required=True, help='New GitHub account for repository URLs')

    # GitClone action
    gitclone_parser = subparsers.add_parser('gitclone', help='Clone a GitHub repository into the main project.')
    gitclone_parser.add_argument('repo_url', nargs='?', help='URL of the GitHub repository to clone')
    gitclone_parser.add_argument('--lang', default='en', help='Language code for the MkDocs project')
    gitclone_parser.add_argument('--project', help='Path to the main project if not in current directory')
    gitclone_parser.add_argument('--batch', help='Path to a file containing multiple repositories to clone')
    gitclone_parser.add_argument('--dry-run', '-d', action='store_true', help='Add repository to mkdocs-lang.yml without cloning')

    # Custom Command Line action
    cl_parser = subparsers.add_parser('cl', help='Execute a custom command across all MkDocs projects.')
    cl_parser.add_argument('command', help='The custom command to execute')
    cl_parser.add_argument('--project', help='Path to the main project if not in current directory')
    cl_parser.add_argument('-y', action='store_true', help='Automatically confirm execution without prompting')

    # Parse arguments
    args = parser.parse_args(args)

    if args.action == 'newproject':
        newproject.create_project(args.project, args.github)
    elif args.action == 'newsite':
        newsite.create_mkdocs_project(args.mkdocs_project, args.lang, args.project)
    elif args.action == 'config':
        config.update_github_account(args.project, args.github)
    elif args.action == 'gitclone':
        if args.batch:
            gitclone.clone_repos_from_file(args.batch, args.project)
        elif args.repo_url:
            gitclone.clone_repo(args.repo_url, args.lang, args.project, args.dry_run)
        else:
            gitclone.clone_repos_from_mkdocs_lang(args.project)
    elif args.action == 'cl':
        cl.execute_command(args.command, args.project, args.y)

if __name__ == '__main__':
    main()
