{{/* Name of every agent object: <release>-agent. */}}
{{- define "agent.fullname" -}}
{{- printf "%s-agent" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "agent.selectorLabels" -}}
app.kubernetes.io/name: armoury-agent
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "agent.labels" -}}
{{ include "agent.selectorLabels" . }}
app.kubernetes.io/part-of: armoury
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end -}}

{{/* The image by digest; rendering fails without one, so nothing floats. */}}
{{- define "agent.image" -}}
{{- $ref := required "agent.image.ref is required (repository@sha256:<digest>)" .Values.image.ref -}}
{{- if not (contains "@sha256:" $ref) -}}
{{- fail (printf "agent.image.ref must be pinned by digest, got %q" $ref) -}}
{{- end -}}
{{- $ref -}}
{{- end -}}
