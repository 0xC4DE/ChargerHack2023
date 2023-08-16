cd ../../chrometokenmanager
go build
mv chrometokenmanager ../solvers/total_tester/
cd ../solvers/total_tester
python encryptdecrpttester.py make
