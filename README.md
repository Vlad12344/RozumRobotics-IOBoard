# Rozum Robotics IO Board v1.0.3 simple Python API

API allows you to connect pc to Rozum Robotics IOBoard and simply make control via input/output commands

## Connect to IOBoard:

                from io_board import IOBoard

                ip = '7.7.7.3'
                port = 23000
                timeout = 0.1

                io = IOBoard(ip=ip, port=port, timeout=timeout)

In default ***timeout*** is 0.1 seconds

***set_digital_output(numberPin: int, state: str)***

Set digital output in 'HIGH'/'LOW' state

                io.set_digital_output(1, 'HIGH')

***get_digital_input(inputPin)***

Get state of entered digital input
Return True or False value. Print 'HIGH' or 'LOW'

                io.get_digital_input(1)
                >>>'LOW'

***get_digital_outputs()***

Return a set() of digital outputs that are in 'HIGH' state

                io.get_digital_outputs()
                >>>(1, 4, 3)

***get_digital_inputs()***

Return a set() of digital inputs that are in 'HIGH' state

                io.get_digital_inputs()
                >>>(2, 3, 5)