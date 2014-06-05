function [curve] = pureflip(flips,A)
curve = [];
for i = 1:flips
    results = A^i;
   curve(i,:) = results(8,:);
end
pureflip=[]
plot (curve, 'DisplayName','curve', 'YDataSource', 'curve');figure(gcf)
