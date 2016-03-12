% ????????????RGB???????????
green=[0,161,111];
green=rgb2hsv(green)
a=imread('./mvtest3.png');
imshow(a)
pause
threshold = 37;
c = zeros      (60 , 80 , 3);
for i = 1 : 3
    temp = imresize(a(: , : , i) , [60 , 80]);
    c(: , : , i) = double(temp);
end
b=zeros(60,80);
for i = 1:60
    for j= 1:80
        color=c(i,j,:);
        color = reshape(color,[1,3]);
        diff = double(color) - double(green);
        diff = norm(diff);
        if (diff<threshold)
            b(i,j)=1;
        end
    end
end
for i = 1:60
    for j = 1:80
    end
end

imshow(b)

