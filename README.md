# self-design-git
## not following the blog but write my own style git
## ./mygit to run the tool
## in the init function (./mygit init) you can specify where to init the git repository, you can reinit the repository by running ./mygit init again
## in the add function (./mygit add) you can specify the files to add, use -all or -A to add all files, files in .git will not be added, when adding file, we create blob in objects and write things in index like real git 
### create a class **git_track_file** to track the file and add to objects and index 
