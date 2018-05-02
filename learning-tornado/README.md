# 91KageWeChat

pip install tornado
pip install wechatpy
pip install pycrypto>=2.6.1
pip install -U wechatpy # for update
pip install MySQL-python
pip install pyconvert
pip install redis


#redis for access_token cache.
sudo apt-get install redis-server
sudo service redis-server start

# mysql --
login root exec.
    CREATE USER 'kageweb'@'%' IDENTIFIED BY 'kageweb';
    GRANT ALL PRIVILEGES ON  *.* TO 'kageweb'@'%' IDENTIFIED BY 'kageweb';
    flush privileges;

login kageweb exec...
    create database kageweb;
    use kageweb;

    source kageweb.sql.

