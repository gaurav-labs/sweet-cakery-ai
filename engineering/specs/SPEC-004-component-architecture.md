LangGraph Mapping

Our Architecture	LangGraph	                Notes

Entry Point	        FastAPI / CLI	                    Starts the workflow
Workflow	        StateGraph	                        Orchestrates the business process
Workflow State	    State	                            One state per workflow
Agent	            Node	                            Stateless reasoning node
Tool	            Tool / Python Function	            Deterministic execution
Connector	        Adapter Class	                    Called by tools
AI Gateway	        Service	                            Used only by agents
Memory	            Checkpointer + Application Memory	Owned by workflow
Human Approval	    Interrupt	                        Resume later
Conditional Logic	Conditional Edges	                Workflow routing
End	                END Node	                        Workflow completed