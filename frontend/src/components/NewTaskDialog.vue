<template>
  <Dialog
    :options="{
      title: 'New Task',
      actions: [
        {
          label: 'Create',
          variant: 'solid',
          onClick: onCreateClick,
        },
      ],
    }"
    v-model="showDialog"
    @after-leave="newTask = initialData"
  >
    <template #body-content>
      <div class="space-y-4">
        <FormControl label="Title" v-model="newTask.title" autocomplete="off" />
        <FormControl
          label="Description"
          type="textarea"
          v-model="newTask.description"
        />
        <div class="flex space-x-2">
          <Dropdown
            :options="
              statusOptions({
                onClick: (status) => (newTask.status = status),
              })
            "
          >
            <Button>
              <template #prefix>
                <TaskStatusIcon :status="newTask.status" />
              </template>
              {{ newTask.status }}
            </Button>
          </Dropdown>

          <Dropdown
            :options="
              priorityOptions({
                onClick: (priority) => (newTask.priority = priority),
              })
            "
          >
            <Button>
              <template #prefix>
                <TaskPriorityIcon :priority="newTask.priority" />
              </template>
              {{ newTask.priority }}
            </Button>
          </Dropdown>

          <TextInput
            type="date"
            placeholder="Set due date"
            v-model="newTask.due_date"
          />
          <!-- Updated by Omar Jaber -->
          <Autocomplete
            placeholder="Assign a user"
            v-model="newTask.assigned_to"
            :options="assignableUsers"
            :value="newTask.assigned_to"
            @change="(option) => (newTask.assigned_to = option?.value || '')"
          />
        </div>

        <!-- Updated by Omar Jaber -->
        <div class="flex space-x-2">
          
          <!-- Is Group Checkbox -->
          <label class="flex items-center space-x-1">
            <input 
              type="checkbox" 
              :checked="newTask.is_group === 1" 
              @click="() => newTask.is_group = newTask.is_group === 1 ? 0 : 1"
              class="form-checkbox"
            />
            <span>Group Task</span>
          </label>

          <!-- Parent Group Task -->
          <Autocomplete
            placeholder="Parent Task"
            v-model="newTask.parent_task"
            :options="GroupTasks"
            @change="(option) => (newTask.parent_task = option?.value || '')"
          />


        </div>

        <ErrorMessage class="mt-2" :message="createTask.error" />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import { ref, computed, h } from 'vue'
import {
  Dialog,
  FormControl,
  Autocomplete,
  Dropdown,
  TextInput,
  createResource,
} from 'frappe-ui'
import TaskStatusIcon from './icons/TaskStatusIcon.vue'
import TaskPriorityIcon from './icons/TaskPriorityIcon.vue'
import { activeUsers } from '@/data/users'
import { activeGroupTasks } from '@/data/group_tasks'

const props = defineProps(['modelValue', 'defaults'])
const emit = defineEmits(['update:modelValue'])
const showDialog = ref(false)
const createTask = createResource({
  url: 'frappe.client.insert',
  makeParams(values) {
    return {
      doc: {
        doctype: 'GP Task',
        ...values,
      },
    }
  },
})
const initialData = {
  title: '',
  description: '',
  status: 'Backlog',
  priority: 'Low',
  is_group: 0,
  assigned_to: null,
  project: null,
}

const newTask = ref(initialData)

function statusOptions({ onClick }) {
  return ['Backlog', 'Todo', 'In Progress', 'Done', 'Canceled'].map(
    (status) => {
      return {
        icon: () => h(TaskStatusIcon, { status }),
        label: status,
        onClick: () => onClick(status),
      }
    },
  )
}

function priorityOptions({ onClick }) {
  return ['Low', 'Medium', 'High', 'Urgent'].map(
    (priority) => {
      return {
        icon: () => h(TaskPriorityIcon, { priority }),
        label: priority,
        onClick: () => onClick(priority),
      }
    },
  )
}

const assignableUsers = computed(() => {
  return activeUsers.value
    .filter((user) => user.name != newTask.value.assigned_to)
    .map((user) => ({
      label: user.full_name,
      value: user.name,
    }))
})


const GroupTasks = computed(() => {
  return activeGroupTasks.value.map((task) => ({
    label: task.label,
    value: task.value,
  }));
})


let _onSuccess
function show({ defaults, onSuccess } = {}) {
  newTask.value = { ...initialData, ...(defaults || {}) }
  showDialog.value = true
  _onSuccess = onSuccess
}

function onCreateClick(close) {

  // Updated by Omar Jaber
  // Make sure assigned_to is just the email (value)
  if (newTask.value.assigned_to && typeof newTask.value.assigned_to === 'object') {
    newTask.value.assigned_to = newTask.value.assigned_to.value; // Ensure it only contains the email (value)
  }

  // Make sure parent_task is just the name (value)
  if (newTask.value.parent_task && typeof newTask.value.parent_task === 'object') {
    newTask.value.parent_task = newTask.value.parent_task.value; // Ensure it only contains the email (value)
  }
  
  console.log('*********')
  console.log(newTask.value)
  console.log('*********')
  

  createTask
    .submit(newTask.value, {
      validate() {
        if (!newTask.value.title) {
          return 'Task title is required'
        }
      },
      onSuccess: _onSuccess,
    })
    .then(close())
}

defineExpose({ show })
</script>
