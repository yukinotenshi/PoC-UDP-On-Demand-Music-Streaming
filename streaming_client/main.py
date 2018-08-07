from streaming_client.client import Client


def intro():
    print("Welcome to [SISTER] Music Stream")
    print("Here you can hear the highest(?) quality we can afford using crappy socket implementation")
    print("Enjoy your MONO, 16kHZ, 8 bit music")


def ask_action():
    print(">> ", end="")
    answer = input()

    return answer


def execute(client: Client, answer: str):
    split_answer = answer.split()
    cmd, args = split_answer[0], split_answer[1:]

    if cmd == "subscribe":
        name = args[0]
        address = (args[1], int(args[2]))
        client.subscribe(name, address)
    elif cmd == "servers":
        for key, _ in client.servers.items():
            print(key)
    elif cmd == "connect":
        client.connect(args[0])
    elif cmd == "songs":
        client.list_song()
        for i, song in enumerate(client.songs):
            print(f"{i}. {song}")
    elif cmd == "play":
        client.play(int(args[0]))
    elif cmd == "pause":
        client.pause()
    elif cmd == "resume":
        client.resume()
    elif cmd == "exit":
        client.stop()
        client.exit()
        exit()
    else:
        print_help()


def print_help():
    print("Available commands :")
    print("1. subscribe <name> <ip> <port>")
    print("2. servers")
    print("3. connect <server_name>")
    print("4. songs")
    print("5. play <song_index>")
    print("6. pause")
    print("7. resume")
    print("8. help")
    print("9. exit")


if __name__ == "__main__":
    socket_client = Client()
    intro()
    while True:
        action = ask_action()
        try:
            execute(socket_client, action)
        except Exception as e:
            print(e)