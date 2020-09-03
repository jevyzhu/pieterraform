variable string_test {
  type        = string
  default     = "jevy"
  description = "A name"
}

variable no_default {
  type        = string
}

variable dict_test {
  type = object({
    internal = number
    external = number
    protocol = string
  })
  default = {
      internal = 8300
      external = 8300
      protocol = "tcp"
  }
}

variable list_test {
  type = list(object({
    internal = number
    external = number
    protocol = string
  }))
  default = [
    {
      internal = 8300
      external = 8300
      protocol = "tcp"
    }
  ]
}