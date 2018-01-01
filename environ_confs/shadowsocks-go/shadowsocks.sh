#sudo -u nobody /home/eric-lin/software/shadowsocks-go/shadowsocks-local-linux64-1.1.4 -c /home/eric-lin/software/shadowsocks-go/config.json
if [ $# -eq 0 ]
then
    #./shadowsocks-local-linux64-1.1.4 &>/dev/null &
    /home/eric-lin/software/shadowsocks-go/shadowsocks-local-linux64-1.1.4 -c /home/eric-lin/software/shadowsocks-go/config.json >/dev/null 2>&1 &
else
    /home/eric-lin/software/shadowsocks-go/shadowsocks-local-linux64-1.1.4 -c $1 >/dev/null 2>&1 &
    #./shadowsocks-local-linux64-1.1.4 -c $1 &>/dev/null &
fi  
