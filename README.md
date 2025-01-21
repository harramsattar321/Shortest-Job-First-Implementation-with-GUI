# Enhanced SJF Process Scheduler Visualization

A Python-based interactive visualization tool for the Shortest Job First (SJF) process scheduling algorithm with an enhanced graphical user interface using Turtle graphics and Matplotlib.

## Features

- 🎯 Interactive process scheduling visualization
- 📊 Real-time process state transitions
- 📈 Gantt chart generation
- 🎨 User-friendly GUI for process input
- ⚡ Dynamic queue management
- 🔄 Process interruption and wait functionality
- 📊 Detailed process statistics

## Requirements

- Python 3.x
- Required libraries:
  - `turtle`
  - `matplotlib`
  - `time`
  - `random`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/sjf-process-scheduler.git
cd sjf-process-scheduler
```

2. Install required dependencies:
```bash
pip install matplotlib
```

## Usage

1. Run the program:
```bash
python process_scheduler.py
```

2. Follow the GUI prompts to:
   - Enter the number of processes (1-10)
   - Specify arrival time and burst time for each process
   - Click "Start" to begin the visualization

3. During simulation:
   - Use the "INTERRUPT" button to interrupt the current process
   - Use the "WAIT" button to move the current process to waiting state

## Program Structure

### Main Classes

#### 1. Process
Represents a process with attributes:
- `pid`: Process ID
- `arrival_time`: Time when process arrives
- `burst_time`: CPU time required
- `remaining_time`: Time left for completion
- `completion_time`: Time when process completes
- `waiting_time`: Total waiting time
- `turnaround_time`: Total time in system
- `state`: Current process state

#### 2. ProcessScheduler
Manages the scheduling simulation with features:
- Process state visualization
- Queue management (Ready, Waiting, Upcoming)
- Interactive state transitions
- Real-time visualization updates
- Gantt chart generation
- Process statistics calculation

#### 3. InputForm
Handles user input through GUI:
- Process count input
- Process details collection
- Input validation
- Visual feedback

### Visualization Components

1. **State Display**
   - Ready state
   - Running state
   - Waiting state
   - Terminated state

2. **Queue Displays**
   - Ready queue
   - Waiting queue
   - Upcoming processes queue

3. **Interactive Elements**
   - INTERRUPT button
   - WAIT button
   - Process movement animations

4. **Statistics and Charts**
   - Gantt chart visualization
   - Process completion statistics
   - Turnaround time analysis
   - Waiting time calculations

## Algorithm Implementation

The scheduler implements the Shortest Job First (SJF) non-preemptive algorithm with additional features:

1. **Process Selection**
   - Selects process with shortest burst time from ready queue
   - Considers only processes that have arrived
   - Non-preemptive execution once started

2. **Queue Management**
   - Maintains separate queues for different process states
   - Handles dynamic process arrivals
   - Manages process state transitions

3. **Interactive Controls**
   - Process interruption capability
   - Wait state management
   - Real-time queue updates

## Technical Details

### Color Scheme
- Background: `#F0F4F8`
- Process States: `#E6CCE6` (Soft lavender)
- Text: `#2D3E50` (Dark blue-gray)
- Buttons: `#98D8AA` (Mint green)

### Performance Considerations
- Uses efficient turtle graphics updates
- Implements smooth animations
- Manages memory through proper object cleanup
- Handles window closure gracefully

## Output

The program generates:
1. Real-time visualization of process scheduling
2. Interactive process movement animations
3. Gantt chart showing process execution timeline
4. Detailed statistics for each process including:
   - Completion time
   - Turnaround time
   - Waiting time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with Python's Turtle graphics library
- Visualization enhanced with Matplotlib
- Inspired by operating system scheduling algorithms
