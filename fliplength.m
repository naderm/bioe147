%Description: Fliplength is a function of A, the adjacency matrix 
%n, the number of pancakes, and p a position vector that takes, 
%in state order, the stack of pancakes. That is put the numerical 
%representation of each possible pancake stack into this vector, 
%every digit seperated, in the same order that represents 
%the states of the adjacency matrix collume 1 to the last collume.   
function fliplength = fliplength(n)
A = oldadjmat(n,2);
sp = signedperms(n)';
p = sp(:)';
for i=1:length(A)
    for j=1:length(A)
        if A(i,j)>0
            counter=0;
            for t=0:n-1
                if p(n*j-t)==p(n*i-t)
                    counter=counter;
                else counter=counter+1;
                end
                fliplength(i,j) = counter;
            end
        else fliplength(i,j) = 0;
        end
    end
end
                    
        
