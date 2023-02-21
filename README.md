# my_media_scripts
Various Scripts to Do Common Things




Personal Reference: Create Repo Sync

Here are the steps to add a Git submodule to your GitHub repository:

    Navigate to your GitHub repository and create a new folder for the submodule.

    In your terminal or command prompt, navigate to your local repository.

    Use the git submodule add command to add the external repository as a submodule. For example:


>>
git submodule add https://github.com/exampleuser/external-repository.git subdirectory-name

The subdirectory-name argument is the name of the folder you created in step 1.

    Stage and commit the changes to your local repository:


>>
git add .
git commit -m "Added external repository as submodule"

    Push the changes to your remote repository:


>>
git push

Once you have completed these steps, the external repository will be included as a submodule in your repository, and changes made to the submodule will be tracked separately from changes made to your main repository.

To update the submodule, you can navigate to the submodule folder and use the git pull command to pull in the latest changes from the external repository.

I hope this helps! Let me know if you have any further questions.