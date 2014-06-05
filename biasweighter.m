%Description: Biasweighter takes as inputs a fliplength matrix,
%telling the length of a flip between any two states in the 
%adjacency matrix if possible, 0 otherwise, and a weights vector, 
%telling the probability of making a flip of length i in its ith term.
%Biasweighter then creates a transition matrix. 
function biasweights = biasweighter(fliplength,weights)
for j=1:length(fliplength)
for k=1:length(fliplength)
for i=0 
if fliplength(j,k)==0
   biasweights(j,k)=0; 
end
end
for i=1:length(fliplength)
if fliplength(j,k)==i
   biasweights(j,k)=weights(i);
end
end
end
end
