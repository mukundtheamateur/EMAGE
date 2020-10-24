Imports System.IO

Public Class Form1

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        PictureBox2.Visible = False
        Label1.Visible = True
        Label2.Visible = True
        Label3.Visible = True
        TextBox1.Visible = True
        TextBox2.Visible = True
        TextBox3.Visible = True
        Button1.Visible = True
        Button2.Visible = True
        Button3.Visible = True

    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If (TextBox1.Text = String.Empty Or TextBox2.Text = String.Empty Or TextBox3.Text = String.Empty) Then
            MessageBox.Show("Please fill in all fields", "Oops")
        Else
            Using sw As StreamWriter = New StreamWriter("log.txt")
                sw.WriteLine(TextBox1.Text)
                sw.WriteLine(TextBox2.Text)
                sw.WriteLine(TextBox3.Text)
            End Using
            Process.Start("cmd", "/c python source_rendition.py")
            TextBox1.Clear()
            TextBox2.Clear()
            TextBox3.Clear()
            PictureBox1.Visible = True
            Button4.Visible = True
            Label4.Visible = True
        End If
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        TextBox1.Clear()
        TextBox2.Clear()
        TextBox3.Clear()
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Me.Close()
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        PictureBox1.BackgroundImage = Image.FromFile("result.png")
    End Sub
End Class
