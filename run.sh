#!/bin/bash


lazy="1"


if [ "$lazy" =  "1" ];
  then
  echo ""
  echo ""
  echo "you're a lazy and didnt edited run.sh with the variables to connect, please edit run.sh and set lazy variable as \"0\""
  echo ""
  echo ""
  exit
fi



export CB_NICKNAME="lamebot" #your nickname
export CB_IDENTD="itsame"   #your identd
export CB_HOST="irc.lameserver.org" #server
export CB_CHANNEL="##lamechannel" #channel



#optional variables uncomment below if you need then


#if you need to auth on server uncomment below and put your password
#this is a secure measure that you dont put your passwd in any file of the bot
#but still acessible with "echo $cb_user password"

#export CB_USER_PASSWD=""

#to use our weather command you need OpenWeather API key
#uncomment below and put between ""

#export OPEN_WEATHER_API=""


#if you dont want to auth to nickserv just uncomment below and put 0


#export CB_NICKSERV_AUTH=1



while true
do
python run.py
sleep 1
done
