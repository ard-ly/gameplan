import { computed } from "vue";
import { createListResource } from "frappe-ui";

// Fetching group tasks (is_group = 1)
export let groupTasks = createListResource({
  doctype: "GP Task",
  fields: ["name", "title", "is_group", "project", "assigned_to", "status"],
  filters: [["is_group", "=", 1]],
  orderBy: "title asc",
  pageLength: 999,
  cache: "GroupTasks",
  transform(tasks) {
    return tasks.map((task) => {
      return {
        label: task.title,
        value: task.name,
        project: task.project,
        assigned_to: task.assigned_to,
      };
    });
  },
  auto: true,
});

// All group tasks
export let activeGroupTasks = computed(
  () => groupTasks.data || [],
);

// Get group tasks for a specific project (optional utility function)
export function getProjectGroupTasks(project) {
  return activeGroupTasks.value.filter((task) => task.project === project) || [];
}

// Find a specific group task by name (optional utility function)
export function getGroupTask(taskId) {
  return groupTasks.data.find((task) => task.name.toString() === taskId.toString());
}
