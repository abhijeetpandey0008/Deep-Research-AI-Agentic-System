from dotenv import load_dotenv
load_dotenv()

from graph_workflow import build_graph

def main():
    graph_app = build_graph()
    user_query = input("Enter a research query: ")

    print("\n  Researching...\n")
    result = graph_app.invoke({"question": user_query})

    print("\n Final Answer:\n")
    print(result["final_answer"])

if __name__ == "__main__":
    main()
