% HSV?????
green = [0.4409, 1, 0.6196];
% green = rgb2hsv(green)
a = imread('./.png');
imshow(a);
pause;
a = rgb2hsv(a);
a = double(a)
%threshold = 37;
%????
c = zeros(60, 80, 3);
for i = 1 : 3
    temp = imresize(a(: , : , i) , [60 , 80]);
    c(: , : , i) = double(temp);
end
%V??
for i = 1 : 480
    for j = 1: 640
        color = a(i, j, :);
        if (abs(color(1) - green(1)) > 0.1)       
            color(3) = color(3)/3;
        end
        a(i, j, :) = color;
    end
end
imshow(hsv2rgb(a))

b=zeros(60, 80);
threshold = 1
for i = 1 : 60
    for j= 1 : 80
        color = c(i, j, :);
        color = reshape(color, [1,3]);
        diff = double(color) - double(green);
        diff = norm(diff);
        if (diff<threshold)
            b(i,j)=1;
        end
    end
end

imshow(b)


