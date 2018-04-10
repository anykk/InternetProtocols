import scala.io.StdIn

//116951205

object Main extends App {
  override def main(args: Array[String]): Unit = {
    val id = StdIn.readLine("Enter user's id: ").toInt
    FriendsExample.getInfo(id).foreach(s => println(s))
  }
}