nohup uwsgi --ini /opt/bitcoin_project/bitcoinweb/uwsgi_config.ini  &
/opt/nginx/sbin/nginx
service iptables stop
