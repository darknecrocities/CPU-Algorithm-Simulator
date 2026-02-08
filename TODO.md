# Task: Make Priority Input Optional for FCFS, SJF, and Round Robin

## Plan:
- [x] Analyze current implementation
- [x] Modify `ui/inputs.py` to make Priority input conditional
- [x] Test the application to ensure all algorithms work correctly
- [x] Verify Priority algorithm still requires priority values
- [x] Ensure FCFS, SJF, and Round Robin work without priority input

## Changes Completed:
1. ✅ Moved algorithm selection before process input fields
2. ✅ Made Priority input field conditional based on selected algorithm
3. ✅ Assigned default priority value (1) when not using Priority algorithm
4. ✅ Updated column layout for 2 or 3 columns based on algorithm

## Summary:
- **FCFS, SJF, Round Robin**: Now only show Arrival Time (AT) and Burst Time (BT) inputs
- **Priority Algorithm**: Shows all three inputs including Priority (Pr)
- **Default Priority**: Non-priority algorithms automatically assign priority=1 to all processes
- **Backward Compatibility**: Predefined scenarios still work with all algorithms
