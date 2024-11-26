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

        <!-- Updated by Omar Jaber -->

        <!-- New Team dropdown -->
        <Autocomplete
          placeholder="Select team"
          v-model="newTask.team"
          :options="UsersTeams"
          @update:modelValue="onTeamChange"
        />

        <!-- New Project dropdown -->
        <Autocomplete
          placeholder="Select project"
          v-model="newTask.project"
          :options="filteredProjects"
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
        <ErrorMessage class="mt-2" :message="createTask.error" />
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import { ref, computed, h, watch } from 'vue'
import {
  Dialog,
  FormControl,
  Autocomplete,
  Dropdown,
  TextInput,
  createResource,
} from 'frappe-ui'
import TaskStatusIcon from './icons/TaskStatusIcon.vue'
import { activeUsers } from '@/data/users'
import { teams } from '@/data/teams'
import { activeProjects } from '@/data/projects'

const props = defineProps(['modelValue', 'defaults'])
const emit = defineEmits(['update:modelValue'])
const showDialog = ref(false)


const createTask = createResource({
  url: 'frappe.client.insert',
  makeParams(values) {
    console.log(values)
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
  assigned_to: null,
  team: null,
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


// Updated by Omar Jaber

// Directly use imported `teams` for team options
const UsersTeams = computed(() =>
  Array.isArray(teams.data)
    ? teams.data.map((team) => ({
        label: team.title,
        value: team.name,
      }))
    : []
);



// Filter and format active projects for Autocomplete
const UsersProjects = computed(() =>
  Array.isArray(activeProjects.value)
    ? activeProjects.value.map((project) => ({
        label: project.title, // Use the project title as the display label
        value: project.name, // Use the project name as the unique value
        team: project.team, // Include the team to filter later
      }))
    : []
);

// Dynamically filter projects based on selected team
const filteredProjects = computed(() => {
  if (!newTask.value.team) {
    return []; // Return an empty array if no team is selected
  }

  // Filter projects based on the selected team
  return UsersProjects.value.filter((project) => project.team === newTask.value.team.value);
});


function onTeamChange() {
  newTask.value.project = null; // Clear selected project when team changes
}





const assignableUsers = computed(() => {
  return activeUsers.value
    .filter((user) => user.name != newTask.value.assigned_to)
    .map((user) => ({
      label: user.full_name,
      value: user.name,
    }))
})






let _onSuccess
function show({ defaults, onSuccess } = {}) {
  newTask.value = { ...initialData, ...(defaults || {}) }

  // Updated by Omar Jaber
  // If there is an initial project, set the team and project
  if (defaults && defaults.project) {
    const initialProject = activeProjects.value.find(project => project.name === Number(defaults.project));
    if (initialProject) {
      newTask.value.team = { label: initialProject.team, value: initialProject.team }; // Set the team based on the project
      newTask.value.project = { label: initialProject.title, value: initialProject.name }; // Set the project
    }
  }

  showDialog.value = true
  _onSuccess = onSuccess
}


function onCreateClick(close) {
  // Updated by Omar Jaber
  // Make sure assigned_to is just the email (value)
  if (newTask.value.assigned_to && typeof newTask.value.assigned_to === 'object') {
    newTask.value.assigned_to = newTask.value.assigned_to.value; // Ensure it only contains the email (value)
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
