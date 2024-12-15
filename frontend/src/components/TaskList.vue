<template>
  <div class="@container" v-if="tasks.data?.length">
    {{ console.log(groupedTasks) }}
    <div v-for="group in groupedTasks" :key="group.title">
      <button
        class="group flex w-full items-baseline rounded-sm bg-gray-50 px-2.5 py-2 text-base transition hover:bg-gray-100"
        v-if="group.title && group.tasks.length"
        @click="isOpen[group.title] = !isOpen[group.title]"
      >
        <span class="font-medium text-gray-900">
          {{ group.title }}
        </span>
        <span class="ml-2 text-sm text-gray-600">{{ group.tasks.length }}</span>
        <span class="ml-auto hidden text-sm text-gray-600 group-hover:inline">
          {{ isOpen[group.title] ? 'Collapse' : 'Expand' }}
        </span>
      </button>


      <div :class="{ hidden: !(isOpen[group.title] ?? true) }">
        
        <!-- Updated by Omar Jaber -->
        <div v-for="(d, index) in group.tasks" :key="d.name">

          <div 
            v-if="
              !d.is_group && !d.parent_task
            ">
          
          <router-link
            :to="{
              name: d.project ? 'ProjectTaskDetail' : 'Task',
              params: { teamId: d.team, projectId: d.project, taskId: d.name },
            }"
            class="flex h-15 w-full items-center rounded p-2.5 transition hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
            :class="{
              'pointer-events-none':
                tasks.delete.loading && tasks.delete.params.name === d.name,
            }"
            
          >
            <div class="w-full">
              <div class="flex min-w-0 items-start">
                <LoadingIndicator
                  class="h-4 w-4 text-gray-600"
                  v-if="
                    tasks.delete.loading && tasks.delete.params.name === d.name
                  "
                />
                <Tooltip text="Change status" v-else>
                  <Dropdown
                    :options="
                      statusOptions({
                        onClick: (status) =>
                          tasks.setValue.submit({
                            status,
                            name: d.name,
                          }),
                      })
                    "
                  >
                    <button
                      class="flex rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
                    >
                      <TaskStatusIcon :status="d.status" />
                    </button>
                  </Dropdown>
                </Tooltip>
                <div
                  class="ml-2.5 overflow-hidden text-ellipsis whitespace-nowrap text-base font-medium leading-4 text-gray-900"
                >
                  {{ d.title }}
                </div>
                <div
                  class="ml-auto shrink-0 whitespace-nowrap text-sm text-gray-600"
                >
                  {{ $dayjs(d.modified).fromNow() }}
                </div>
              </div>

              <div class="ml-6.5 mt-1.5 flex items-center">
                <div class="text-base text-gray-600">#{{ d.name }}</div>
                <div
                  v-if="$route.name != 'ProjectOverview' && d.project"
                  class="flex min-w-0 items-center text-base leading-none text-gray-600"
                >
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div>{{ d.team_title }}</div>
                  <LucideChevronRight class="h-3 w-3 shrink-0 text-gray-600" />
                  <div class="overflow-hidden text-ellipsis whitespace-nowrap">
                    {{ d.project_title }}
                  </div>
                </div>
                <div class="hidden items-center @md:flex" v-if="d.assigned_to">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <span class="whitespace-nowrap text-base text-gray-600">
                    {{ $user(d.assigned_to).full_name }}
                  </span>
                </div>

                <template v-if="d.due_date">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div class="flex items-center">
                    <LucideCalendar class="h-3 w-3 text-gray-600" />
                    <span
                      class="ml-2 whitespace-nowrap text-base text-gray-600"
                    >
                      {{ $dayjs(d.due_date).format('D MMM') }}</span
                    >
                  </div>
                </template>
                <template v-if="d.priority">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div class="flex items-center">
                    <div
                      class="h-2 w-2 rounded-full"
                      :class="{
                        'bg-red-800': d.priority === 'Urgent',
                        'bg-orange-500': d.priority === 'High',
                        'bg-yellow-500': d.priority === 'Medium',
                        'bg-gray-300': d.priority === 'Low',
                      }"
                    ></div>
                    <span class="ml-2 text-base text-gray-600">
                      {{ d.priority }}
                    </span>
                  </div>
                </template>
                <div
                  class="ml-auto inline-grid h-4 w-4 shrink-0 place-items-center rounded-full bg-gray-200 text-xs"
                  :class="[
                    d.unread ? 'text-gray-900' : 'text-gray-600',
                    d.comments_count ? '' : 'invisible',
                  ]"
                >
                  {{ d.comments_count || 0 }}
                </div>
              </div>
            </div>
          </router-link>
        </div>


          <div
            class="mx-2.5 border-b"
            v-if="index < group.tasks.length - 1"
          ></div>
        </div>


        <!-- Updated by Omar Jaber -->
        
        <div v-for="(d, index) in group.child_tasks" :key="d.name">
          <div>
            <div
              class="flex w-full items-center rounded p-2.5 transition hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
              >
              <div class="w-full">
                <div class="flex min-w-0 items-start">
                  <div
                    class="overflow-hidden text-ellipsis whitespace-nowrap text-base font-medium leading-4 text-gray-900"
                    style="width: 15%;"
                  > 
                    {{ d.title }}
                  </div>
                  <!-- progress bra start -->
                  <div class="progress" v-if="showProgressBar">
                    <div 
                      class="progress-bar progress-bar-success progress-bar-striped" 
                      role="progressbar"
                      :aria-valuenow="d.completion_percent"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      :style="{ width: d.completion_percent + '%' }"
                    >
                      {{ d.completion_percent }}% Complete
                    </div>
                  </div>
                  <!-- progress bra ends -->

                </div>
              </div>
          </div>
          <!-- Updated by Omar Jaber -->


          <router-link
            v-for="(d, index) in d.tasks"
            :to="{
              name: d.project ? 'ProjectTaskDetail' : 'Task',
              params: { teamId: d.team, projectId: d.project, taskId: d.name },
            }"
            class="flex h-15 w-full items-center rounded p-2.5 transition hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
            :class="{
              'pointer-events-none':
                tasks.delete.loading && tasks.delete.params.name === d.name,
            }"
            :style="d.parent_task ? 'padding-left:2rem' : ''"
            
          >
            <div class="w-full">
              <div class="flex min-w-0 items-start">
                <LoadingIndicator
                  class="h-4 w-4 text-gray-600"
                  v-if="
                    tasks.delete.loading && tasks.delete.params.name === d.name
                  "
                />
                <Tooltip text="Change status" v-else>
                  <Dropdown
                    :options="
                      statusOptions({
                        onClick: (status) =>
                          tasks.setValue.submit({
                            status,
                            name: d.name,
                          }),
                      })
                    "
                  >
                    <button
                      class="flex rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
                    >
                      <TaskStatusIcon :status="d.status" />
                    </button>
                  </Dropdown>
                </Tooltip>
                <div
                  class="ml-2.5 overflow-hidden text-ellipsis whitespace-nowrap text-base font-medium leading-4 text-gray-900"
                >
                  {{ d.title }}
                </div>
                <div
                  class="ml-auto shrink-0 whitespace-nowrap text-sm text-gray-600"
                >
                  {{ $dayjs(d.modified).fromNow() }}
                </div>
              </div>

              <div class="ml-6.5 mt-1.5 flex items-center">
                <div class="text-base text-gray-600">#{{ d.name }}</div>
                <div
                  v-if="$route.name != 'ProjectOverview' && d.project"
                  class="flex min-w-0 items-center text-base leading-none text-gray-600"
                >
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div>{{ d.team_title }}</div>
                  <LucideChevronRight class="h-3 w-3 shrink-0 text-gray-600" />
                  <div class="overflow-hidden text-ellipsis whitespace-nowrap">
                    {{ d.project_title }}
                  </div>
                </div>
                <div class="hidden items-center @md:flex" v-if="d.assigned_to">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <span class="whitespace-nowrap text-base text-gray-600">
                    {{ $user(d.assigned_to).full_name }}
                  </span>
                </div>

                <template v-if="d.due_date">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div class="flex items-center">
                    <LucideCalendar class="h-3 w-3 text-gray-600" />
                    <span
                      class="ml-2 whitespace-nowrap text-base text-gray-600"
                    >
                      {{ $dayjs(d.due_date).format('D MMM') }}</span
                    >
                  </div>
                </template>
                <template v-if="d.priority">
                  <div class="px-2 leading-none text-gray-600">&middot;</div>
                  <div class="flex items-center">
                    <div
                      class="h-2 w-2 rounded-full"
                      :class="{
                        'bg-red-800': d.priority === 'Urgent',
                        'bg-orange-500': d.priority === 'High',
                        'bg-yellow-500': d.priority === 'Medium',
                        'bg-gray-300': d.priority === 'Low',
                      }"
                    ></div>
                    <span class="ml-2 text-base text-gray-600">
                      {{ d.priority }}
                    </span>
                  </div>
                </template>
                <div
                  class="ml-auto inline-grid h-4 w-4 shrink-0 place-items-center rounded-full bg-gray-200 text-xs"
                  :class="[
                    d.unread ? 'text-gray-900' : 'text-gray-600',
                    d.comments_count ? '' : 'invisible',
                  ]"
                >
                  {{ d.comments_count || 0 }}
                </div>
              </div>
            </div>
          </router-link>
          </div>





          <div
            class="mx-2.5 border-b"
            v-if="index < group.tasks.length - 1"
          ></div>
          </div>



        <!-- Updated by Omar Jaber -->
      </div>
    </div>
  </div>
  <div
    class="flex flex-col items-center rounded-lg border-2 border-dashed py-8 text-base text-gray-600"
    v-else
  >
    No tasks
  </div>
</template>
<script>
import { h } from 'vue'
import { LoadingIndicator, Dropdown, Tooltip } from 'frappe-ui'
import TaskStatusIcon from './icons/TaskStatusIcon.vue'

export default {
  name: 'TaskList',
  props: {
    groupByStatus: {
      type: Boolean,
      default: false,
    },
    listOptions: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      isOpen: {
        Backlog: true,
        Todo: true,
        'In Progress': true,
        Canceled: false,
        Done: false,
      },
    }
  },
  components: {
    LoadingIndicator,
    Dropdown,
    Tooltip,
    TaskStatusIcon,
  },
  resources: {
    tasks() {
      return {
        type: 'list',
        url: 'gameplan.gameplan.doctype.gp_task.gp_task.get_list',
        cache: ['Tasks', this.listOptions],
        doctype: 'GP Task',
        fields: [
          '*',
          'project.title as project_title',
          'team.title as team_title',
        ],
        filters: this.listOptions.filters,
        orderBy: this.listOptions.orderBy || 'creation desc',
        pageLength: this.listOptions.pageLength || 20,
        auto: true,
        realtime: true,
      }
    },
  },
  methods: {
    statusOptions({ onClick }) {
      return ['Backlog', 'Todo', 'In Progress', 'Done', 'Canceled'].map(
        (status) => {
          return {
            icon: () => h(TaskStatusIcon, { status }),
            label: status,
            onClick: () => onClick(status),
          }
        }
      )
    },
  },
  computed: {
    tasks() {
      return this.$resources.tasks
    },
    showProgressBar() {
      return this.$route.path.includes('tasks');
    },
    groupedTasksOld() {
      if (!this.groupByStatus) {
        return [
          {
            id: 'all',
            title: '',
            tasks: this.tasks.data,
          },
        ]
      }
      return ['In Progress', 'Todo', 'Backlog', 'Done', 'Canceled'].map(
        (status) => {
          return {
            id: status,
            title: status,
            tasks: this.tasksByStatus[status] || [],
          }
        }
      )
    },
    groupedTasks() {
      if (!this.tasks?.data?.length) {
        return [];
      }

      const statuses = ['In Progress', 'Todo', 'Backlog', 'Done', 'Canceled'];
      const groupedTasks = [];
      const allGroupTasks = {}; // Store all group tasks globally across statuses
      const taskMapByParent = {}; // **NEW: Map parent task IDs to their child tasks**


      // Preprocess all group tasks
      this.tasks.data.forEach(task => {
        if (task.is_group) {
          allGroupTasks[task.name] = {
            id: task.name,
            title: task.title
          };
        }
      });


      // **NEW: Build a mapping of parent_task to its child tasks**
      this.tasks.data.forEach(task => {
        if (task.parent_task) {
          if (!taskMapByParent[task.parent_task]) {
            taskMapByParent[task.parent_task] = [];
          }
          taskMapByParent[task.parent_task].push(task);
        }
      });


      // Group tasks by statuses
      statuses.forEach(status => {
        const tasksInStatus = this.tasksByStatus?.[status] || [];
        const groupedByParent = {};
        const nonGroupTasks = [];

        // Update groupTasks with each group task, where task.name is the key and value is an object containing task details
        tasksInStatus.forEach(task => {
          if (task.is_group) {
            // Initialize the group task
            groupedByParent[task.name] = groupedByParent[task.name] || {
              title: task.title,
              id: task.name,
              completion_percent: 0.0,
              tasks: []
            };
          }
        });


        tasksInStatus.forEach(task => {
          const parentTaskId = task.parent_task;

          if (task.is_group) {
            // Initialize the group task and add it as a parent task
            groupedByParent[task.name] = groupedByParent[task.name] || {
              title: task.title, // Use the group's own title
              id: task.name,
              completion_percent: 0.0,
              tasks: [],
            };
          }


          if (parentTaskId) {
            // Check if the parent task exists in the group
            if (!groupedByParent[parentTaskId]) {
              // Check if this parent task is a group task, then use its title
              const parentGroup = allGroupTasks[parentTaskId];

              // Initialize the parent task group if not already present
              groupedByParent[parentTaskId] = {
                title: parentGroup?.title || 'Unknown Parent',
                id: parentGroup?.id || parentTaskId,
                completion_percent: 0.0,
                tasks: [],
              };
            }

            // Add the task to its parent group
            groupedByParent[parentTaskId].tasks.push(task);

            // Add non-group tasks Also to show length and show the status
            nonGroupTasks.push(task);
          } else if(!task.is_group){
            // Add non-group tasks (tasks without parent_task) directly to their status
            nonGroupTasks.push(task);
          }
        });


        // **NEW: Calculate completion_percent for all groups in the status**
        Object.keys(allGroupTasks).forEach(parentId => {
          const childTasks = taskMapByParent[parentId] || []; // Get all child tasks for this group
          const totalTasks = childTasks.length; // Total number of child tasks
          const completedTasks = childTasks.filter(task => task.status == 'Done').length; // Tasks with 'Done' status
          const completionPercent = totalTasks > 0 
            ? Math.round((completedTasks / totalTasks) * 100) 
            : 0;

          // Update the groupedByParent with the completion percent
          if (groupedByParent[parentId]) {
            groupedByParent[parentId].completion_percent = completionPercent;
            //groupedByParent[parentId].tasks = childTasks; // Attach the child tasks
          }
        });


        // Add the status group
        groupedTasks.push({
          id: status,
          title: status,
          tasks: nonGroupTasks, // Only non-group tasks here
          child_tasks: Object.values(groupedByParent).filter(group => group.tasks.length > 0), // Groups with children in this status
        });
      });

      return groupedTasks;
    },
    groupedIsGroup() {
      if (!this.groupByStatus) {
        return [
          {
            id: 'all',
            title: '',
            tasks: this.tasks.data,
          },
        ]
      }

      const groupedTasks = {};

      this.tasks.data.forEach(task => {
        if (task.is_group) {
          groupedTasks[task.name] = {
            id: task.name,
            title: task.title,
            tasks: [],
          };
        } else {
          const parentTaskId = task.parent_task;
          if (parentTaskId && groupedTasks[parentTaskId]) {
            groupedTasks[parentTaskId].tasks.push(task);
          }
        }
      });

      return Object.values(groupedTasks);
    },
    tasksByStatus() {
      const tasksByStatus = {}
      this.tasks.data.forEach((task) => {
        if (!tasksByStatus[task.status]) {
          tasksByStatus[task.status] = []
        }
        tasksByStatus[task.status].push(task)
      })
      return tasksByStatus
    },
  },
}
</script>


<style scoped>
  /* Progress Bar Container */
  .progress {
    height: 1.2rem; /* Height of the progress bar */
    background-color: #f3f3f3; /* Background color */
    border-radius: 0.25rem; /* Rounded corners */
    width: 100%; /* Full width */
  }

  /* Progress Bar */
  .progress-bar {
    display: flex;
    height: 100%; /* Full height of the container */
    transition: width 0.6s ease; /* Smooth transition for width */
    text-align: center;
    white-space: nowrap;
    color: #fff; /* Text color inside the bar */
    font-size: 0.875rem; /* Text size inside the bar */
    line-height: 1.5rem; /* Text alignment in the bar */
    background-color: #28a745; /* Default color, green */
    border-radius: 0.25rem;
    padding-right: 5px;
    padding-left: 5px;
  }

  /* Success (Green) for progress-bar-success */
  .progress-bar-success {
    background-color: #28a745; /* Bootstrap success color */
  }

  /* Striped effect for progress-bar-striped */
  .progress-bar-striped {
    background-image: linear-gradient(45deg, rgba(255, 255, 255, .15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, .15) 50%, rgba(255, 255, 255, .15) 75%, transparent 75%, transparent);
    background-size: 40px 40px; /* Stripe size */
    animation: progress-bar-stripes 1s linear infinite; /* Animation for stripes */
  }

  /* Animation for stripes */
  @keyframes progress-bar-stripes {
    0% { background-position: 40px 0; }
    100% { background-position: 0 0; }
  }

</style>

