#TODO

    TIMES

    morphlogy kernal

    动态中心

    画幅

    图像去边框

    向量长度

    落点在前方

    下位机保护代码
		-> Systick Interrupts中设置累加器，UART Interrupts中置零，当累加至一定大小时自动停车。
		-> DONE

	运动电机PID -> 上位机完成
		->  DONE

#安装

    sudo apt-get install libopencv-dev

#编译

    make cv_chase

#运行

    ./cv_chase

#测试

    我用笔记本的摄像头，测试绿色的水瓶盖，基本能捕捉到，但是不知道方向反了没有

#FIXME

    搜索一下`FIXME`
    一些opencv的函数，有可能参数传反了，比如长宽传成了宽长

#使用说明
	
	make main & ./main   #测试摄像头
	make cv_chase & ./cv_chase  #调整色彩捕获算法
	make vector_test & ./vector_test #测试运动预测算法
	make car_test & ./car_test #测试上位机pid
	make vector & ./vector  #主程序运行
	
