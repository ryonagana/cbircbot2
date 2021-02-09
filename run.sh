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



export cb_nickname="lamebot" #your nickname
export cb_identd="itsame"   #your identd
export cb_host="irc.lameserver.org" #server
export cb_channel="##lamechannel" #channel



#optional variables uncomment below if you need then


#if you need to auth on server uncomment below and put your password
#this is a secure measure that you dont put your passwd in any file of the bot
#but still acessible with "echo $cb_user password"

#export cb_user_passwd=""   

#to use our weather command you need OpenWeather API key
#uncomment below and put between ""

#export open_weather_api=""


#if you dont want to auth to nickerv just uncomment below and put 0


#export cb_nickserv_auth=1



while true
do
python run.py
sleep 1
done
