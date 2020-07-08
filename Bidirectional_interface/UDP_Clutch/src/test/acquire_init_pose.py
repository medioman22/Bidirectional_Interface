import context
import HRI_communication as comm

comm.setup_sockets()

comm.acquire_store_init_pose()

comm.close_sockets()