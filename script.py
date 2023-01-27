# import os
# import sys
# from main import main
# path= sys.argv[1]
# if os.path.exists(path):
#     main(path)
#     #print(os.path.basename(fn))
c=0
for i in range(41,81):
    c+=1/i

print(1-c)