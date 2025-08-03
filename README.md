# self-design-git
## not following the blog but write my own style git
## ./mygit to run the tool
## in the init function (./mygit init) you can specify where to init the git repository, you can reinit the repository by running ./mygit init again
## in the add function (./mygit add) you can specify the files to add, use -all or -A to add all files, files in .git will not be added, when adding file, we create blob in objects and write things in index like real git 
### create a class **git_track_file** to track the file and add to objects and index 
#### 8.2 in the index, I only store file path and content hash
## add a ls-index command to list the index, it will show the file path and content hash
## decide not write binary, write just strings and integers
## solve the problem add same file twice, it will not add the same file again, but update the content hash in index
## doing it in a bruteforce way,read index every add time and compare every thing, recreate objects every time 
# in commit, bruteforce over index and find file path and hash we want 
## decide not to write binary, but just write string
