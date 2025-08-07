# agents.tf
resource "aws_instance" "agent_node" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "g4dn.xlarge"  # GPU optimized
  tags = {
    Name = "phind-agent-${var.env}"
  }
  
  lifecycle {
    prevent_destroy = true
  }
}