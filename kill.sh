#ps aux | grep Baichuan
#ps aux | grep model_server |  awk '{print $2}' | xargs kill -9
ps aux | grep HomeCat |  awk '{print $2}' | xargs kill -9
