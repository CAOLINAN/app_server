# app_server
using IPFS and ulord to create a single a blog

# install
## install python and pip
firstly you need install python2.7 from the [website](https://www.python.org/)

secondly install pip to manager your python packages

thirdly using pip to install packages
```bash
pip install -r requirements.txt
```
## install go-ipfs
You can use Tools/ipfs/install.bat to install ipfs.It will copy the ipfs.exe to your system environment.
> warnning:It will copy the file to C:\Windows\System32.So if your system environment is not there you should modify the bat file handly and excute it.

go-ipfs is a tool of ipfs.You can connect the ipfs using it.Change the config and you can connect the ulord's IPFS.

You can download IPFS form [here](https://github.com/ipfs/go-ipfs/releases/tag/v0.4.14)

And then you need set the environment variables including the ipfs.

Then using the command to init your ipfs(Windows):
```bash
ipfs init
ipfs bootstrap rm --all
ipfs bootstrap add /ip4/114.67.37.2/tcp/20418/ipfs/QmctwnuHwE8QzH4yxuAPtM469BiCPK5WuT9KaTK3ArwUHu
ipfs config Datastore.StorageMax "1MB"
ipfs daemon
```
This is a daemon program.Don't exit!

# run
```bash
python dbHelper\dbManager.py

python Using_API.py publish <your file path>

python Using_API.py download <youre hash>
```


