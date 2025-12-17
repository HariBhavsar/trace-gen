# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Non-Inclusive -w 40000000 -i 100000000 ./pr-twitter-120K-2.trace.xz > data/pr-twitter/120K/log_summary_Non-Inclusive_pr-twitter-120K-2.out
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Exclusive -w 40000000 -i 100000000 ./pr-twitter-120K-2.trace.xz > data/pr-twitter/120K/log_summary_Exclusive_pr-twitter-120K-2.out
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Re-Exclusive -w 40000000 -i 100000000 ./pr-twitter-120K-2.trace.xz > data/pr-twitter/120K/log_summary_Re-Exclusive_pr-twitter-120K-2.out &

# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Non-Inclusive -w 40000000 -i 100000000 ./pr-twitter-120K-3.trace.xz > data/pr-twitter/120K/log_summary_Non-Inclusive_pr-twitter-120K-3.out & 
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Exclusive -w 40000000 -i 100000000 ./pr-twitter-120K-3.trace.xz > data/pr-twitter/120K/log_summary_Exclusive_pr-twitter-120K-3.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Re-Exclusive -w 40000000 -i 100000000 ./pr-twitter-120K-3.trace.xz > data/pr-twitter/120K/log_summary_Re-Exclusive_pr-twitter-120K-3.out &

# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Non-Inclusive -w 40000000 -i 100000000 ./pr-twitter-30K-1.trace.xz > data/pr-twitter/30K/log_summary_Non-Inclusive_pr-twitter-30K-1.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-1.trace.xz > data/pr-twitter/30K/log_summary_Exclusive_pr-twitter-30K-1.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Re-Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-1.trace.xz > data/pr-twitter/30K/log_summary_Re-Exclusive_pr-twitter-30K-1.out &

# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Non-Inclusive -w 40000000 -i 100000000 ./pr-twitter-30K-2.trace.xz > data/pr-twitter/30K/log_summary_Non-Inclusive_pr-twitter-30K-2.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-2.trace.xz > data/pr-twitter/30K/log_summary_Exclusive_pr-twitter-30K-2.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Re-Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-2.trace.xz > data/pr-twitter/30K/log_summary_Re-Exclusive_pr-twitter-30K-2.out &

# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Non-Inclusive -w 40000000 -i 100000000 ./pr-twitter-30K-3.trace.xz > data/pr-twitter/30K/log_summary_Non-Inclusive_pr-twitter-30K-3.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-3.trace.xz > data/pr-twitter/30K/log_summary_Exclusive_pr-twitter-30K-3.out &
# ../ReExclusive-refurbished/Champsims/BaseChampSim-Re-Exclusive/bin/Re-Exclusive -w 40000000 -i 100000000 ./pr-twitter-30K-3.trace.xz > data/pr-twitter/30K/log_summary_Re-Exclusive_pr-twitter-30K-3.out &

python3 generate-bbv.py pr web 
python3 generate-bbv.py pr kron 
python3 generate-bbv.py pr road 
python3 generate-bbv.py pr urand 