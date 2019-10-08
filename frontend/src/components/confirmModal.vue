<template>
	<v-layout row wrap>
		<v-dialog
			:value=true
			persistent
			@keydown.esc="$emit('close')"
			:overlay="false"
			max-width="500px"
			@close="contentDeleteConfirmation = false"
			transition="dialog-transition">
			<v-card>
				<v-card-title class="background elevation-4 py-1">
					<span class="headline">
						{{ toolbarMsg }}
					</span>
					<v-spacer></v-spacer>
					<v-btn icon @click="$emit('close')">
						<v-icon>close</v-icon>
					</v-btn>
				</v-card-title>
				<v-card-text>
					{{ bodyMsg }}
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn depressed :ref="cancelBtnText" @click="$emit('close')">
						{{ cancelBtnText }}
					</v-btn>
					<v-btn depressed :ref="okBtnText" color="primary" class="background--text" @click="$emit('action', data); $emit('close')">
						{{ okBtnText }}
					</v-btn>
					</v-card-actions>
			</v-card>
		</v-dialog>
	</v-layout>
</template>

<script>

export default {
	props: ['toolbarMsg', 'bodyMsg', 'okBtnText', 'cancelBtnText', 'autofocus'],
	data () {
		return {
			data: ''
		}
	},
	mounted () {
		if (this.autofocus) {
			this.$refs[this.autofocus].$el.focus()
		}
	}
}
</script>
