import Task from "./Task";
import AddTask from "./AddTask";

function TaskList() {
    return (
        <>
            <h3>TaskList Rendered!</h3>
            <Task />
            <Task />
            <Task />
            <AddTask />
        </>
    )
}

export default TaskList;