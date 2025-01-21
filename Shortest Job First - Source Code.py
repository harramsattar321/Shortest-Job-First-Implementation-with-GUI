import turtle
import matplotlib.pyplot as plt
import time
import random

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.started = False
        self.state = 'ready'
        self.arrived = False

class ProcessScheduler:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Enhanced SJF Process Scheduler")
        self.screen.setup(1200, 800)
        self.screen.bgcolor("#F0F4F8")
        
        self.state_colors = {
            'ready': '#E6CCE6',    
            'running': '#E6CCE6',    
            'waiting': '#E6CCE6',    
            'terminated': '#E6CCE6'  # Soft lavender
        }
        
        # Initialize turtles and queues before creating UI elements
        self.process_turtle = turtle.Turtle()
        self.process_turtle.penup()
        self.process_turtle.shape("circle")
        self.process_turtle.color("gray")
        
        self.info_turtle = turtle.Turtle()
        self.info_turtle.hideturtle()
        self.info_turtle.penup()
        
        self.ready_queue = []
        self.waiting_queue = []
        self.upcoming_queue = []
        self.processes = []
        self.terminated_processes = set()
        
        self.interrupt_occurred = False
        self.wait_requested = False
        
        # Create UI elements
        self.states = self.create_states()
        self.queue_displays = self.create_queue_displays()
        self.create_buttons()

    def create_state_turtle(self, x, y, state_name, color): 
        state = turtle.Turtle()
        state.penup()
        state.goto(x, y)
        state.shape("square")
        state.shapesize(3, 6)
        state.color("#2D3E50", color)
        
        label = turtle.Turtle()
        label.hideturtle()
        label.penup()
        label.goto(x, y + 35)
        label.color("#2D3E50")
        label.write(state_name, align="center", font=("Arial", 14, "bold"))
        
        return state

    def create_states(self):
        return {
            'ready': self.create_state_turtle(-200, 100, "Ready", self.state_colors['ready']),
            'running': self.create_state_turtle(0, 100, "Running", self.state_colors['running']),
            'waiting': self.create_state_turtle(0, -100, "Waiting", self.state_colors['waiting']),
            'terminated': self.create_state_turtle(200, 100, "Terminated", self.state_colors['terminated'])
        }

    def create_queue_display(self, x, y, title):
        display = turtle.Turtle()
        display.hideturtle()
        display.penup()
        
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.goto(x, y + 30)
        title_turtle.color("#5B7B7A")
        title_turtle.write(title, align="left", font=("Arial", 14, "bold"))
        
        return display

    def create_queue_displays(self):
        return {
            'ready': self.create_queue_display(-500, 50, "Ready Queue"),
            'waiting': self.create_queue_display(100, -150, "Waiting Queue"),
            'upcoming': self.create_queue_display(-500, -150, "Upcoming Processes")
        }

    def create_button(self, x, y, width, height, text, color):
        button = turtle.Turtle()
        button.hideturtle()
        button.penup()
        
        button.goto(x - width/2, y)
        button.pendown()
        button.fillcolor(color)
        button.begin_fill()
        for _ in range(2):
            button.forward(width)
            button.right(90)
            button.forward(height)
            button.right(90)
        button.end_fill()
        
        button.penup()
        button.goto(x, y - height/1.5)
        button.color("#FFFFFF")
        button.write(text, align="center", font=("Arial", 12, "bold"))

    def create_buttons(self):
        self.create_button(0, -180, 200, 40, "INTERRUPT", "#98D8AA")
        self.create_button(0, -250, 200, 40, "WAIT", "#98D8AA")

    def handle_click(self, x, y):
        if -100 < x < 100:
            if -200 < y < -160:
                self.interrupt_occurred = True
            elif -270 < y < -230:
                self.wait_requested = True

    def update_queue_display(self, queue_type):
        display = self.queue_displays[queue_type]
        display.clear()
        
        if queue_type == 'ready':
            x, y = -500, 50
            processes = [p for p in self.ready_queue if p.pid not in self.terminated_processes]
        elif queue_type == 'waiting':
            x, y = 100, -150
            processes = self.waiting_queue
        else:  # upcoming
            x, y = -500, -150
            processes = self.upcoming_queue
        
        for i, process in enumerate(processes):
            display.goto(x, y - i * 25)
            display.color("#5B7B7A")
            info_text = f"P{process.pid} (Arrival: {process.arrival_time}, Burst: {process.burst_time})"
            display.write(info_text, font=("Arial", 12, "bold"))

    def move_process(self, from_state, to_state, pid):
        if from_state == to_state:
            return
            
        start_pos = self.states[from_state].pos()    
        end_pos = self.states[to_state].pos()
        
        steps = 30
        dx = (end_pos[0] - start_pos[0]) / steps
        dy = (end_pos[1] - start_pos[1]) / steps
        
        self.process_turtle.goto(start_pos)
        self.process_turtle.showturtle()
        
        colors = 'gray'
        
        for i in range(steps):
            current_x = self.process_turtle.xcor() + dx
            current_y = self.process_turtle.ycor() + dy
            self.process_turtle.goto(current_x, current_y)
            
            self.process_turtle.color(colors)
            
            self.info_turtle.clear()
            self.info_turtle.goto(current_x, current_y + 20)
            self.info_turtle.write(f"P{pid}", align="center", font=("Arial", 12, "bold"))
            
            self.screen.update()
            time.sleep(0.05)
        
        if to_state == 'terminated':
            self.terminated_processes.add(pid)
            self.process_turtle.hideturtle()
            self.info_turtle.clear()
            self.update_queue_display('ready')
        elif to_state in ['ready', 'waiting']:
            self.update_queue_display(to_state)

    def add_process(self, process):
        self.processes.append(process)
        if process.arrival_time == 0:
            self.ready_queue.append(process)
            self.update_queue_display('ready')
        else:
            self.upcoming_queue.append(process)
            self.update_queue_display('upcoming')

    def check_arrivals(self, current_time):
        newly_arrived = []
        for process in self.upcoming_queue[:]:
            if process.arrival_time <= current_time and not process.arrived:
                process.arrived = True
                newly_arrived.append(process)
                self.upcoming_queue.remove(process)
                self.ready_queue.append(process)
        
        if newly_arrived:
            self.update_queue_display('upcoming')
            self.update_queue_display('ready')
            return True
        return False

    def schedule_processes(self):
        current_time = 0
        completed_processes = []
        gantt_data = []
        current_process = None
        
        self.screen.onclick(self.handle_click)
        
        while len(completed_processes) < len(self.processes):
            # Check for new arrivals
            self.check_arrivals(current_time)
            
            # If no process is running, select the shortest job from ready queue
            if current_process is None and self.ready_queue:
                # Filter for arrived processes
                active_processes = [p for p in self.ready_queue 
                                 if p.pid not in self.terminated_processes 
                                 and p.arrival_time <= current_time]
                
                if not active_processes:
                    current_time += 1
                    self.screen.update()
                    continue
                
                # Sort by burst time (SJF)
                active_processes.sort(key=lambda x: x.burst_time)
                current_process = active_processes[0]
                
                if not current_process.started:
                    self.move_process('ready', 'running', current_process.pid)
                    current_process.started = True
                
                execution_start = current_time
                execution_time = 0
                
                while execution_time < current_process.burst_time:
                    # Check for new arrivals but don't preempt
                    self.check_arrivals(current_time + execution_time)
                    
                    if self.interrupt_occurred:
                        self.interrupt_occurred = False
                        current_process.burst_time -= execution_time
                        if current_process.pid not in self.terminated_processes:
                            self.move_process('running', 'ready', current_process.pid)
                            current_process = None
                        break

                    if self.wait_requested:
                        self.wait_requested = False
                        current_process.burst_time -= execution_time
                        self.waiting_queue.append(current_process)
                        self.ready_queue.remove(current_process)
                        self.move_process('running', 'waiting', current_process.pid)
                        time.sleep(1)
                        
                        self.waiting_queue.remove(current_process)
                        if current_process.pid not in self.terminated_processes:
                            self.ready_queue.append(current_process)
                            self.move_process('waiting', 'ready', current_process.pid)
                        current_process = None
                        break
                    
                    execution_time += 1
                    time.sleep(0.1)
                    self.screen.update()
                
                if current_process and execution_time == current_process.burst_time:
                    gantt_data.append((current_process.pid, execution_start, 
                                     execution_start + execution_time))
                    
                    current_process.completion_time = current_time + execution_time
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    
                    self.ready_queue.remove(current_process)
                    self.move_process('running', 'terminated', current_process.pid)
                    completed_processes.append(current_process)
                    current_process = None
                
                current_time += execution_time
            else:
                current_time += 1
                self.screen.update()
        
        return gantt_data, completed_processes
    
    def plot_gantt_chart(self, gantt_data, completed_processes):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        colors = ['#FF69B4', '#4169E1', '#32CD32', '#DDA0DD', '#FFA500']
        
        for i, (pid, start, end) in enumerate(gantt_data):
            ax1.barh(y=0, width=end-start, left=start, 
                    color=colors[pid % len(colors)], alpha=0.8)
            ax1.text((start + end)/2, 0, f'P{pid}', 
                    ha='center', va='center', fontweight='bold', color='white')
            
        ax1.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax1.set_title('SJF Schedule Gantt Chart', fontsize=14, fontweight='bold')
        ax1.set_yticks([])
        ax1.grid(True, alpha=0.3)
        
        stats_text = "Process Statistics:\n\n"
        for process in completed_processes:
            stats_text += f"Process {process.pid}:\n"
            stats_text += f"Arrival Time: {process.arrival_time}\n"
            stats_text += f"Completion Time: {process.completion_time}\n"
            stats_text += f"Turnaround Time: {process.turnaround_time}\n"
            stats_text += f"Waiting Time: {process.waiting_time}\n\n"
        
        ax2.text(0.05, 0.95, stats_text, 
                transform=ax2.transAxes, 
                verticalalignment='top',
                fontfamily='monospace')
        ax2.axis('off')   
        
        plt.tight_layout()
        plt.show()

class InputForm:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Process Input Form")
        self.screen.setup(600, 400)
        self.screen.bgcolor("#F0F4F8")
        
        self.input_turtle = turtle.Turtle()
        self.input_turtle.hideturtle()
        self.input_turtle.penup()
        self.input_turtle.color("#2D3E50")  # Dark blue-gray text
        
        self.processes = []
        self.input_complete = False
        
        self.get_process_count()
    
    def draw_button(self, x, y, width, height, text):
        # -50, 0, 100, 40, "Submit"
        self.input_turtle.goto(x, y)
        self.input_turtle.pendown()
        self.input_turtle.setheading(0)
        
        for _ in range(2):
            self.input_turtle.forward(width)
            self.input_turtle.right(90)
            self.input_turtle.forward(height)
            self.input_turtle.right(90)
            
        self.input_turtle.penup()
        self.input_turtle.goto(x + width/2, y - height/1.5)
        self.input_turtle.write(text, align="center", font=("Arial", 12, "bold"))

    def get_process_count(self):
        self.input_turtle.clear()
        
        self.input_turtle.goto(0, 150)
        self.input_turtle.write("SJF Process Scheduler", align="center", font=("Arial", 20, "bold"))
        
        self.input_turtle.goto(0, 100)
        self.input_turtle.write("Enter Number of Processes (1-10):", align="center", font=("Arial", 14))
        
        self.draw_button(-50, 0, 150, 40, "Enter Process")
        
        self.screen.onclick(self.handle_process_count_click)
    
    def handle_process_count_click(self, x, y):
        if -50 < x < 50 and -40 < y < 40:
            try:
                num = int(self.screen.textinput("Process Count", "Enter number of processes (1-10):"))
                if 1 <= num <= 10:
                    self.get_process_details(num)
                else:
                    self.screen.textinput("Error", "Please enter a number between 1 and 10")
                    self.get_process_count()
            except (ValueError, TypeError):
                self.screen.textinput("Error", "Please enter a valid number")
                self.get_process_count()
    
    def get_process_details(self, num_processes):
        self.input_turtle.clear()
        
        self.input_turtle.goto(0, 150)
        self.input_turtle.write("Enter Process Details", align="center", font=("Arial", 20, "bold"))
        
        for i in range(num_processes):
            try:
                arrival_time = int(self.screen.textinput(f"Process {i+1}", 
                    f"Enter arrival time for Process {i+1}:"))
                if arrival_time < 0:
                    raise ValueError
                
                burst_time = int(self.screen.textinput(f"Process {i+1}", 
                    f"Enter burst time for Process {i+1} (in seconds):"))
                if burst_time <= 0:
                    raise ValueError
                    
                process = Process(i+1, arrival_time, burst_time)
                self.processes.append(process)
                
                self.input_turtle.goto(0, 100 - i*30)
                self.input_turtle.write(
                    f"Process {i+1}: Arrival Time = {arrival_time}, Burst Time = {burst_time}s", 
                    align="center", font=("Arial", 12))
                
            except (ValueError, TypeError):
                self.screen.textinput("Error", "Please enter valid positive numbers")
                self.processes = []  # Clear any processes already added
                return self.get_process_details(num_processes)
        
        self.draw_button(-50, -150, 100, 40, "Start")
        self.screen.onclick(self.handle_start_click)
    
    def handle_start_click(self, x, y):
        if -50 < x < 50 and -180 < y < -110:
            self.input_complete = True
            self.screen.clear()

def main():
    try:
        input_form = InputForm()
        
        while not input_form.input_complete:
            input_form.screen.update()
        
        scheduler = ProcessScheduler()
        
        for process in input_form.processes:
            scheduler.add_process(process)
        
        gantt_data, completed_processes = scheduler.schedule_processes()
        scheduler.plot_gantt_chart(gantt_data, completed_processes)
        
        scheduler.screen.mainloop()
        
    except turtle.Terminator:
        print("Window closed by user")

if __name__ == "__main__":
    main()